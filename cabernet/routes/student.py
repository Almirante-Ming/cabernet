from flask import Blueprint, request, jsonify
from cabernet.config import db
from cabernet.models.student import Student
from cabernet.models.course import Course
from http import HTTPStatus

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    name = data.get('name')
    course_id = data.get('course_id')

    if not name or not course_id:
        return jsonify({'message': 'Nome e ID do curso são obrigatórios.'}), HTTPStatus.BAD_REQUEST

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.BAD_REQUEST

    try:
        new_student = Student(name=name, course_id=course_id) #type: ignore
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Estudante criado com sucesso!', 'student': {'id': new_student.id, 'name': new_student.name, 'course_id': new_student.course_id}}), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao criar estudante: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@student_bp.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    students_data = [{'id': student.id, 'name': student.name, 'course_id': student.course_id} for student in students]
    return jsonify(students_data), HTTPStatus.OK

@student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Estudante não encontrado.'}), HTTPStatus.NOT_FOUND
    return jsonify({'id': student.id, 'name': student.name, 'course_id': student.course_id}), HTTPStatus.OK

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Estudante não encontrado.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    name = data.get('name')
    course_id = data.get('course_id')

    if not name and not course_id:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), HTTPStatus.BAD_REQUEST

    if name:
        student.name = name
    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.BAD_REQUEST
        student.course_id = course_id

    try:
        db.session.commit()
        return jsonify({'message': 'Estudante atualizado com sucesso!', 'student': {'id': student.id, 'name': student.name, 'course_id': student.course_id}}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao atualizar estudante: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Estudante não encontrado.'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Estudante excluído com sucesso!'}), HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao excluir estudante: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR