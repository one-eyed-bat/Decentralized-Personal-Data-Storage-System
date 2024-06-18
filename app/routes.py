from flask import render_template, flash ,redirect, request, url_for, Blueprint, jsonify, current_app, session, url_for
#from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
from .models import User
from . import db
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/protected', methods=['GET', 'POST'])
def protected():
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200


@main_bp.route('/')
@main_bp.route('/index')
def index():

    return render_template("index.html", title='Home Page') 


@main_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    response = redirect(url_for('auth_bp.login'))
    for key in request.cookies:
        response.set_cookie(key, '', expires=0)
    return redirect(url_for('main_bp.index'))
@main_bp.route('/user')
def user():
    return render_template("user.html")
@main_bp.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)
@main_bp.route("/users/create", methods=["GET", "POST"])
def user_create():
    pass 

