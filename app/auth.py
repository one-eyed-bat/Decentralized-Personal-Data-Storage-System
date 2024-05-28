from flask import render_template, Flask, request, jsonify, session, redirect, url_for, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import User
from . import db, bcrypt
import os
from dotenv import load_dotenv
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user

load_dotenv()
auth_bp= Blueprint('auth_bp', __name__)

#SECRET = os.getenv('SECRET')

#app = Flask(__name__)
#app.config['JWT_SECRET_KEY'] = 'SECRET'
#jwt = JWTManager(app)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('register.html', title='Register', form=RegistrationForm())
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401


    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=form.remember_me.data)
#       next_page = request.args.get('next')
#       if not next_page or urlsplit(next_page).netloc != '':
        next_page = url_for('main_bp.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! You are now a registered user!')
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html', title='Register', form=form)







