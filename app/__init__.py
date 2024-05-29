from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
login = LoginManager()



## I have commented out the line because of a circular import problem. Not sure exactly what
## the porblem was, but I believe I imported the routes and models for a different tutorial.
## so let's hope the commenting out doesn't fuck anything up.


#from app import routes, models


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)  
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'auth_bp.login'
    

    from app.routes import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    

    return app


   
#with app.app_context():
#    db.create_all()

