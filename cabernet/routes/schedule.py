from flask import Blueprint, request, jsonify
from cabernet.config import db
from cabernet.models.schedule import Schedule
from cabernet.models.users import User
from cabernet.models.lab import Lab
from cabernet.models.course import Course
from http import HTTPStatus

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.get_json()
    requerent_id = data.get('requerent_id')
    lab_id = data.get('lab_id')
    course_id = data.get('course_id')

    if not requerent_id or not lab_id or not course_id:
        return jsonify({'message': 'IDs do requerente, laboratório e curso são obrigatórios.'}), HTTPStatus.BAD_REQUEST

    user = User.query.get(requerent_id)
    if not user:
        return jsonify({'message': 'Requerente (usuário) não encontrado.'}), HTTPStatus.BAD_REQUEST

    lab = Lab.query.get(lab_id)
    if not lab:
        return jsonify({'message': 'Laboratório não encontrado.'}), HTTPStatus.BAD_REQUEST

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.BAD_REQUEST

    try:
        new_schedule = Schedule(requerent_id=requerent_id, lab_id=lab_id, course_id=course_id) #type: ignore
        db.session.add(new_schedule)
        db.session.commit()
        return jsonify({'message': 'Agendamento criado com sucesso!', 'schedule': {'id': new_schedule.id, 'requerent_id': new_schedule.requerent_id, 'lab_id': new_schedule.lab_id, 'course_id': new_schedule.course_id}}), HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao criar agendamento: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@schedule_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    schedules = Schedule.query.all()
    schedules_data = []
    for schedule in schedules:
        schedules_data.append({
            'id': schedule.id,
            'requerent_id': schedule.requerent_id,
            'lab_id': schedule.lab_id,
            'course_id': schedule.course_id
        })
    return jsonify(schedules_data), HTTPStatus.OK

@schedule_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'message': 'Agendamento não encontrado.'}), HTTPStatus.NOT_FOUND
    return jsonify({'id': schedule.id, 'requerent_id': schedule.requerent_id, 'lab_id': schedule.lab_id, 'course_id': schedule.course_id}), HTTPStatus.OK

@schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'message': 'Agendamento não encontrado.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    requerent_id = data.get('requerent_id')
    lab_id = data.get('lab_id')
    course_id = data.get('course_id')

    if not requerent_id and not lab_id and not course_id:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), HTTPStatus.BAD_REQUEST

    if requerent_id:
        user = User.query.get(requerent_id)
        if not user:
            return jsonify({'message': 'Requerente (usuário) não encontrado.'}), HTTPStatus.BAD_REQUEST
        schedule.requerent_id = requerent_id
    if lab_id:
        lab = Lab.query.get(lab_id)
        if not lab:
            return jsonify({'message': 'Laboratório não encontrado.'}), HTTPStatus.BAD_REQUEST
        schedule.lab_id = lab_id
    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Curso não encontrado.'}), HTTPStatus.BAD_REQUEST
        schedule.course_id = course_id

    try:
        db.session.commit()
        return jsonify({'message': 'Agendamento atualizado com sucesso!', 'schedule': {'id': schedule.id, 'requerent_id': schedule.requerent_id, 'lab_id': schedule.lab_id, 'course_id': schedule.course_id}}), HTTPStatus.OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao atualizar agendamento: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'message': 'Agendamento não encontrado.'}), HTTPStatus.NOT_FOUND

    try:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'message': 'Agendamento excluído com sucesso!'}), HTTPStatus.NO_CONTENT
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao excluir agendamento: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR