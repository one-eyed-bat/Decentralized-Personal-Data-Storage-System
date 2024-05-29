from flask import render_template, Flask, request, jsonify, session, redirect, url_for, Blueprint, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import User
from . import db, bcrypt
import os
from dotenv import load_dotenv
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from .utils import data_encrypt
import sqlalchemy as sa


auth_bp= Blueprint('auth_bp', __name__)

@login_required
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

        
#        data = request.get_json()
#        username = data['username']
#        password = data['password']
#        user = User.query.filter_by(username=username).first()
#        if user and user.check_password(password):
#            access_token = create_access_token(identity=user.id)
#            return jsonify(access_token=access_token), 200
#        else:
#            return jsonify(message="Invalid credentials"), 401


    if request.method == 'POST':
        
        if form.validate_on_submit():
            user = db.session.scalar(
                    sa.select(User).where(User.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth_bp.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main_bp.index')
                return redirect(next_page)
    return render_template('login.html', title='Sign In', form=LoginForm())


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', title='Register', form=RegistrationForm())
    
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! You are now a registered user!')
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html', title='Register', form=form)


auth_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_encrypted_data():
   with open(file_path, 'rb') as f:
       file_content = f.read()

   encrypted_data_dict = data_encrypt(file_content)
    # logic to upload the file to ipfs

   os.remove(file_path)

   return jsonify({'message': 'File uploaded and encrypted successfully'}), 200




