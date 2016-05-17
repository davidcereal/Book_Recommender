from flask import Flask, render_template
from flask.ext.wtf import Form
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_app.config import config
from flask.ext.login import LoginManager
from flask import Blueprint
from flask_wtf.csrf import CsrfProtect
#from flask_alembic import Alembic

#alembic = Alembic()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
#login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
csrf = CsrfProtect()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	moment.init_app(app)
	db.init_app(app)
	csrf.init_app(app)
	#alembic.init_app(app)

	login_manager.init_app(app)

	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .recommender import recommender as recommender_blueprint
	app.register_blueprint(recommender_blueprint )

	return app


