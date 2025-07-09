from flask import Blueprint, request, jsonify
from cabernet.config import db, User_type
from cabernet.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

user_bp = Blueprint('user_crud', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    u_type = data.get('u_type', User_type.USER.value)

    if not name or not email or not password:
        return jsonify({'message': 'Nome, email e senha são obrigatórios.'}), HTTPStatus.BAD_REQUEST

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Usuário com este email já existe.'}), HTTPStatus.CONFLICT

    hashed_password = generate_password_hash(password, method='scrypt')

    try:
        new_user = User(name=name, email=email, u_type=User_type(u_type), password=hashed_password) #type: ignore
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso!', 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'u_type': new_user.u_type.value}}), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao criar usuário: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'u_type': user.u_type.value} for user in users]
    return jsonify(users_data), HTTPStatus.OK

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), HTTPStatus.NOT_FOUND
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'u_type': user.u_type.value}), HTTPStatus.OK

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    u_type = data.get('u_type')

    if not name and not email and not password and not u_type:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), HTTPStatus.BAD_REQUEST

    if name:
        user.name = name
    if email:
        existing_user_with_email = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user_with_email:
            return jsonify({'message': 'Este email já está em uso por outro usuário.'}), HTTPStatus.CONFLICT
        user.email = email
    if password:
        user.password = generate_password_hash(password, method='scrypt')
    if u_type:
        try:
            user.u_type = User_type(u_type)
        except ValueError:
            return jsonify({'message': 'Tipo de usuário inválido.'}), HTTPStatus.BAD_REQUEST

    try:
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso!', 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'u_type': user.u_type.value}}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao atualizar usuário: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso!'}), HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao excluir usuário: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR