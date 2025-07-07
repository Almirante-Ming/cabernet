from cabernet.config import db, User_type
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from cabernet.models import User
from flask_jwt_extended import create_access_token
from http import HTTPStatus

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    u_type = data.get('u_type', User_type.USER.value)

    if not name or not password:
        return jsonify({'message': 'Nome de usuário e senha são obrigatórios.'}), HTTPStatus.BAD_REQUEST

    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return jsonify({'message': 'Usuário com este nome já existe.'}), HTTPStatus.CONFLICT

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = User(name=name, u_type=User_type(u_type), password_hash=hashed_password) #type: ignore
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), HTTPStatus.CREATED

@auth.route('/login', methods=['POST'])
def login_auth():
    data = request.get_json()
    login_id = data.get('identification')
    login_pass = data.get('password')

    user = User.query.filter_by(name=login_id).first()

    if user and check_password_hash(user.password_hash, login_pass):
        access_token = create_access_token(identity={'id': user.id, 'name': user.name, 'u_type': user.u_type.value})
        return jsonify(access_token=access_token), HTTPStatus.OK
    else:
        return jsonify({'message': 'Credenciais inválidas.'}), HTTPStatus.FORBIDDEN