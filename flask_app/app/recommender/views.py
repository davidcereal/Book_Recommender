from flask import render_template, session, redirect, url_for, g, request, jsonify
from . import recommender
from .. import db
from ..models import User, Book, Read
from config import Config
from flask.ext.login import login_required, current_user
from flask_wtf.csrf import CsrfProtect


@recommender.route('/recommendations', methods=['GET', 'POST']) 
def recommendations():
