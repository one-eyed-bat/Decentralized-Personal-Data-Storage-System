from flask import render_template, Flask, request, jsonify, session, redirect, url_for, Blueprint, flash, make_response
from flask_session import Session
from .models import User
from . import db, bcrypt
import os
import json
from dotenv import load_dotenv
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from .utils import data_encrypt, data_decrypt, dict_to_mongodb, decrypt_mongodb
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from config import basedir
import ipfs_api

auth_bp= Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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
            session['username'] = user.username
            session['userid'] = user.id
            print(session)
            return render_template('upload.html')
        print(form.errors)
        print("form not validated properly??")
        return render_template('login.html')
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
        print("session at upload func is: ", session)
        user_name = session.get('username')
        user_id = session.get('userid')
        print("Username is: ",user_name, "user ID is: ",user_id )
        if not user_id:
            print("couldn't find session userid")
        else:
            print("userid from session is: ", user_id)

        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 404

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'})
       
        filename = secure_filename(file.filename)
        upload_folder =  os.path.join(basedir, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename) 
        file.save(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
            encrypted_data_dict = data_encrypt(file_content, user_id)
            encrypted_data = encrypted_data_dict['encrypted_data']
            dbname =  dict_to_mongodb(encrypted_data_dict, user_name)
            print(dbname)


            return render_template('upload.html')




            '''#cid = ipfs_api.publish(file_path)
            encrypted_file_path = os.path.join(upload_folder, f"encrypted_{filename}")
            with open(encrypted_file_path, 'w') as f:
                f.write(encrypted_data)
            print("written data?", encrypted_data)
            dict_to_mongodb
            #user_id.data_hash = cid
            print('ipfs id is: ', ipfs_api.my_id())
            with open(os.path.join(upload_folder, 'encrypted_data_dict.json'), 'w') as f:
                json.dump(encrypted_data_dict, f)
            return render_template('decrypt.html')
            os.remove(file_path)
            print(cid, user_name, filename)
            return jsonify({'message': 'File uploaded and encrypted successfully'}), 200'''
    if request.method == 'GET':
        return render_template('upload.html')

@auth_bp.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    user_input = input("retrieve data?")
    if user_input == "yes":
        user_name = session.get('username')
        user_id = session.get('userid')
        print("Username is: ",user_name, "user ID is: ",user_id )
        if not user_id:
            print("couldn't find session userid")
        else:
            print("userid from session is: ", user_id)
        

        en_dict = decrypt_mongodb(user_id, user_name)
        print("at decrypt funciton, returning encrypted dict", en_dict)
        
        return render_template('upload.html')
        file = request.files['file']
        filename = file.filename
        upload_folder =  os.path.join(basedir, 'uploads')
        file_path = os.path.join(upload_folder, filename) 
        
        with open(file_path, 'rb') as f:
            decrypted_data_dict = json.load(f)
            decrypted_data = data_decrypt(decrypted_data_dict)
            print("written data: ", decrypted_data)
        return render_template('upload.html')
    if request.method == 'GET':
        return render_template('decrypt.html')
