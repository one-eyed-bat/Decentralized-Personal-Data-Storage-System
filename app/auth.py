from flask import render_template, Flask, request, jsonify, session, redirect, url_for, Blueprint, flash, make_response
from .models import User
from . import db, bcrypt
import os
from dotenv import load_dotenv
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from .utils import data_encrypt 
import sqlalchemy as sa


def create_jwt():
    access_token = create_access_token(identity=current_user.id)


auth_bp= Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(response)
        return render_template('upload.html')
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.scalar(
                    sa.select(User).where(User.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth_bp.login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main_bp.index')
                return next_page 
            return render_template('login.html', title='Sign In', form=LoginForm())
    return render_template('login.html', title='Sign in', form=LoginForm())

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
        user_id = User.id
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html', title='Register', form=form)



@auth_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print(user_id)
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'message': 'No JWT'})

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'})

        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 404

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'})
       
        filename = secure_filename(file.filename)
        upload_folder =  os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename) 
        file.save(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
            encrypted_data_dict = data_encrypt(file_content, user_id)
            cid = ipfs_api.publish(file)
            user_name = user_id.name
            user_id.data_hash = cid

            os.remove(file_path)
            print(cid, user_name, filename)
            return jsonify({'message': 'File uploaded and encrypted successfully'}), 200
    if request.method == 'GET':
        return render_template('upload.html')



