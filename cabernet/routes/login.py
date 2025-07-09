from cabernet.config import db, User_type
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from cabernet.models.users import User
from flask_jwt_extended import create_access_token
from http import HTTPStatus

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    u_type = data.get('u_type', User_type.USER.value)

    if not name or not email or not password:
        return jsonify({'message': 'all fields are required'}), HTTPStatus.BAD_REQUEST

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'user aready exists'}), HTTPStatus.CONFLICT

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = User(name=name, email=email, u_type=User_type(u_type), password=hashed_password) #type: ignore
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'user created'}), HTTPStatus.CREATED

@auth.route('/login', methods=['POST'])
def login_auth():
    data = request.get_json()
    login_email = data.get('email')
    login_pass = data.get('password')

    user = User.query.filter_by(email=login_email).first()

    if user and check_password_hash(user.password, login_pass):
        access_token = create_access_token(identity={'id': user.id, 'name': user.name, 'email': user.email, 'u_type': user.u_type.value}) # Inclua email no JWT
        return jsonify(access_token=access_token), HTTPStatus.OK
    else:
        return jsonify({'message': 'invalid credentials.'}), HTTPStatus.FORBIDDEN