from flask import render_template, session, redirect, url_for, g, request, jsonify
from . import recommender
from .. import db
from ..models import User, Book, Read
from config import Config
from flask.ext.login import login_required, current_user
from flask_wtf.csrf import CsrfProtect
from recommend import Recommend
import recommendation_data
from recommendation_data import book_data, dict_vectorizer_fit, ipca_model



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
    print 'worked!'
    data = request.json
    books_selected = data['books_selected']
    features_list = []
    print books_selected
    g.Recommend = Recommend(user=g.user, db=db, Read=Read, 
                    book_data=book_data, ipca_model=ipca_model, 
                    dict_vectorizer_fit=dict_vectorizer_fit, n_collab_returned=1000)
    g.recommended_books = g.Recommend.recommend_books(books_selected, features_list)
    rec_data = {"recommendations": g.recommended_books}
    return jsonify(rec_data)

         
