from flask import Flask, request, jsonify, session, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

import os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv('SECRET')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'SECRET'
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    print("need to implement user reg code")

@app.route('/login', methods['POST'])
def login():
    print("implement user login")

if __name__ == "__main__:







