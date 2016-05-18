from flask import Flask, render_template, url_for, current_app
from flask.ext.wtf import Form
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_app.config import config, Config
from flask.ext.login import LoginManager
from flask import Blueprint
from flask_wtf.csrf import CsrfProtect
from flask.ext.s3 import FlaskS3
import flask.ext.whooshalchemy



#from flask_alembic import Alembic

#alembic = Alembic()
moment = Moment()
db = SQLAlchemy()
s3 = FlaskS3()



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
csrf = CsrfProtect()
from .models import Book






def create_app(config_name):
    app = Flask(__name__)
    print config
    print db

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    s3.init_app(app)

    moment.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    #alembic.init_app(app)

    login_manager.init_app(app)
    flask.ext.whooshalchemy.whoosh_index(app, Book)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .recommender import recommender as recommender_blueprint
    app.register_blueprint(recommender_blueprint )



    return app


