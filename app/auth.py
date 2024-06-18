from flask import render_template, Flask, request, jsonify, session, redirect, url_for, Blueprint, flash, make_response, Response
from flask_session import Session
from .models import User
from . import db, bcrypt
from dotenv import load_dotenv
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from .utils import data_encrypt, data_decrypt, dict_to_mongodb, decrypt_mongodb
from werkzeug.utils import secure_filename
from config import basedir, Config
import requests
import ipfs_api
import os
import json
import sqlalchemy as sa


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
            print("pre session clearing: ", session)
            session['username'] = user.username
            session['userid'] = user.id
            session.modified = True
            print("after session update ", session)
            return redirect(url_for('auth_bp.upload'))
        print(form.errors)
        print("form not validated properly??")
        return redirect(url_for('auth_bp.login'))
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
    print("session at the start of the uplaod function: ",  session)
    if request.method == 'POST':
        print("session at POST method is: ", session)
        user_name = session.get('username')
        user_id = session.get('userid')
        print("Username is: ",user_name, "user ID is: ",user_id )
        if not user_id:
            print("couldn't find session userid")
            return redirect(url_for('auth_bp.login'))
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
            encrypted_data_dict = data_encrypt(file_content, user_id, filename)
            print("file saved as: ", filename, " Remember the file name for later retrieval")
            encrypted_data = encrypted_data_dict['encrypted_data']
            encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'w') as f:
            f.write(encrypted_data)
            os.remove(file_path)

        print("ipfs id is: ", ipfs_api.my_id())
        cid = ipfs_api.publish(encrypted_file_path)
        print("cid is: ", cid)
        user = db.session.scalar(
               sa.select(User).where(User.username == user_name))
        print("user at upload func is: ", user)
        user.data_hash = cid
        db.session.commit()
        encrypted_data_dict.pop('encrypted_data')
        print("after popping dict ", encrypted_data_dict)
        dict_to_mongodb(encrypted_data_dict, user_name)
        os.remove(encrypted_file_path) 
        return redirect(url_for('auth_bp.decrypt'))


    if request.method == 'GET':
        print("session at GET method is: ", session)
        return render_template('upload.html')

@auth_bp.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if  request.method == 'GET':
        return render_template('decrypt.html')
    if request.method == 'POST':
        filename = request.form['filename']
        user_name = session.get('username')
        user_id = session.get('userid')
        print("filename: ", filename, " user name ", user_name)
        if not user_id:
            print("couldn't find session userid")
        else:
            print("userid from session is: ", user_id)
        user = db.session.scalar(
                sa.select(User).where(User.username == user_name))
        print("user is: ", user)
        cid = user.data_hash
        print("user retirieved CID is: ", cid)
        en_dict = decrypt_mongodb(user_id, user_name, filename)
        print("at decrypt funciton, returning encrypted dict")
        gateway = 'https://ipfs.io/ipfs/'
        file_url = f'{gateway}{cid}'
        response = requests.get(file_url)
        print(response)
        if response.status_code == 200:
            data = response.content
            print("at decryption with the data")

            de_data = data_decrypt(en_dict, data)
            upload_folder =  os.path.join(basedir, 'uploads')
            file_path = os.path.join(upload_folder, user_name) 
            
            with open(file_path + filename, 'wb') as f:
                f.write(de_data)
            return redirect(url_for('auth_bp.upload')) 
        
