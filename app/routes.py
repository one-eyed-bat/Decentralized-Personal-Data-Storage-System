from flask import render_template, flash ,redirect
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')

def index():
    user = {'username': 'Miguel'}
        
    return render_template('index.html', title='Home', user=user) 
@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}', format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    pass 

