from flask import Flask, jsonify
from cabernet.config import db, migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

load_dotenv('.env')

cabernet = Flask(__name__)

cabernet.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
cabernet.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cabernet.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(cabernet)
migrate.init_app(cabernet, db)
jwt = JWTManager(cabernet) 

from cabernet.routes.login import auth as auth_blueprint
cabernet.register_blueprint(auth_blueprint)


@cabernet.route('/', methods=['GET'])
def read_root():
    return jsonify({'message':'working'})

if __name__ == '__main__':
    cabernet.run(debug=True)