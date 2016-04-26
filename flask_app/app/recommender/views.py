from flask import render_template, session, redirect, url_for, g, request, jsonify
from . import recommender
from .. import db
from ..models import User, Book, Read
from config import Config
from flask.ext.login import login_required, current_user
from flask_wtf.csrf import CsrfProtect

with open('engineered_book_data.pkl', 'r') as picklefile:
    book_data = pickle.load(picklefile)

with open('keyword_conversion_dict.pkl', 'r') as picklefile:
    keyword_conversion_dict = pickle.load(picklefile)

with open('DV_fit.pkl', 'r') as picklefile:
    DV_fit = pickle.load(picklefile)

with open('ipca_model.pkl', 'r') as picklefile:
    ipca_model = pickle.load(picklefile)

@recommender.route('/recommendations', methods=['GET', 'POST']) 
	def recommendations():
		if 
