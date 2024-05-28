from flask import render_template, flash ,redirect, request, url_for, Blueprint, jsonify
#from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from . import db


main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username), 200


@main_bp.route('/')
@main_bp.route('/index')
@login_required

def index():
    return render_template("index.html", title='Home Page') 


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))

@main_bp.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@main_bp.route("/users/create", methods=["GET", "POST"])
def user_create():
    pass 

