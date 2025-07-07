from cabernet.config import db
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_auth():
    form_data = request.form
    login_id = form_data.get('identification')
    login_pass = form_data.get('password')
    return {}
    