from flask import render_template, flash ,redirect, request, url_for
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit



@app.route('/')
@app.route('/index')
@login_required

def index():
    return render_template("index.html", title='Home Page') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or passworld')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
#       next_page = request.args.get('next')
#       if not next_page or urlsplit(next_page).netloc != '':
        next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    pass 

