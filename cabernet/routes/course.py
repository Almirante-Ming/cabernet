from flask import Blueprint, request, jsonify
from cabernet.config import db
from cabernet.models.course import Course
from http import HTTPStatus

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    name = data.get('name')
    period = data.get('period')

    if not name or not period:
        return jsonify({'message': 'Nome e período são obrigatórios.'}), HTTPStatus.BAD_REQUEST

    try:
        new_course = Course(name=name, period=period) #type: ignore
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'message': 'Curso criado com sucesso!', 'course': {'id': new_course.id, 'name': new_course.name, 'period': new_course.period}}), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao criar curso: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@course_bp.route('/courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    courses_data = [{'id': course.id, 'name': course.name, 'period': course.period} for course in courses]
    return jsonify(courses_data), HTTPStatus.OK

@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.NOT_FOUND
    return jsonify({'id': course.id, 'name': course.name, 'period': course.period}), HTTPStatus.OK

@course_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    name = data.get('name')
    period = data.get('period')

    if not name and not period:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), HTTPStatus.BAD_REQUEST

    if name:
        course.name = name
    if period:
        course.period = period

    try:
        db.session.commit()
        return jsonify({'message': 'Curso atualizado com sucesso!', 'course': {'id': course.id, 'name': course.name, 'period': course.period}}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao atualizar curso: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Curso excluído com sucesso!'}), HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao excluir curso: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR