from flask import Flask, jsonify
from cabernet.config import db, migrate
from dotenv import load_dotenv
import os

load_dotenv()

cabernet = Flask(__name__)

cabernet.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
cabernet.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(cabernet)
migrate.init_app(cabernet, db)

@cabernet.route('/', methods=['GET'])
def read_root():
    return jsonify({'message':'working'})

if __name__ == '__main__':
    cabernet.run(debug=True)