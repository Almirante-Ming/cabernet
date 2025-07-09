from flask import Blueprint, request, jsonify
from cabernet.config import db
from cabernet.models.lab import Lab
from http import HTTPStatus

lab_bp = Blueprint('lab', __name__)

@lab_bp.route('/labs', methods=['POST'])
def create_lab():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Nome do laboratório é obrigatório.'}), HTTPStatus.BAD_REQUEST

    try:
        new_lab = Lab(name=name) #type:ignore
        db.session.add(new_lab)
        db.session.commit()
        return jsonify({'message': 'Laboratório criado com sucesso!', 'lab': {'id': new_lab.id, 'name': new_lab.name}}), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao criar laboratório: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@lab_bp.route('/labs', methods=['GET'])
def get_all_labs():
    labs = Lab.query.all()
    labs_data = [{'id': lab.id, 'name': lab.name} for lab in labs]
    return jsonify(labs_data), HTTPStatus.OK

@lab_bp.route('/labs/<int:lab_id>', methods=['GET'])
def get_lab(lab_id):
    lab = Lab.query.get(lab_id)
    if not lab:
        return jsonify({'message': 'Laboratório não encontrado.'}), HTTPStatus.NOT_FOUND
    return jsonify({'id': lab.id, 'name': lab.name}), HTTPStatus.OK

@lab_bp.route('/labs/<int:lab_id>', methods=['PUT'])
def update_lab(lab_id):
    lab = Lab.query.get(lab_id)
    if not lab:
        return jsonify({'message': 'Laboratório não encontrado.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), HTTPStatus.BAD_REQUEST

    lab.name = name

    try:
        db.session.commit()
        return jsonify({'message': 'Laboratório atualizado com sucesso!', 'lab': {'id': lab.id, 'name': lab.name}}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao atualizar laboratório: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@lab_bp.route('/labs/<int:lab_id>', methods=['DELETE'])
def delete_lab(lab_id):
    lab = Lab.query.get(lab_id)
    if not lab:
        return jsonify({'message': 'Laboratório não encontrado.'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(lab)
        db.session.commit()
        return jsonify({'message': 'Laboratório excluído com sucesso!'}), HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao excluir laboratório: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR