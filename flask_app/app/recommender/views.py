from flask import render_template, session, redirect, url_for, g, request, jsonify
from . import recommender
from .. import db
from ..models import User, Book, Read
from config import Config
from flask.ext.login import login_required, current_user
from flask_wtf.csrf import CsrfProtect

'''with open('engineered_book_data.pkl', 'r') as picklefile:
    book_data = pickle.load(picklefile)

with open('DV_fit.pkl', 'r') as picklefile:
    dict_vectorizer_fit = pickle.load(picklefile)

with open('ipca_model.pkl', 'r') as picklefile:
    ipca_model = pickle.load(picklefile)'''

@recommender.before_request
def before_request():
    g.user = current_user



@recommender.route('/recommendations', methods=['GET', 'POST']) 
@login_required
def recommendations():
	return render_template('recommendations.html', current_user=g.user, db=db, Book=Book)

@recommender.route('/recommendations/results', methods=['GET', 'POST']) 
@login_required
def results():
	g.Recommend = Recommend(db=db, Read=Read, books_selected=books_selected)
	g.recommended_books = g.Recommend.recommend_books(book_ids=books_selected, book_data=book_data, 
						ipca_model=ipca_model, dict_vectorizer_fit=dict_vectorizer_fit, 
						n_collab_returned=1000)
	return recommended_books

		 
