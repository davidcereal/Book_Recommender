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
import os




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
    g.data = request.json
    g.data = g.data['recommendation_data'][0]
    g.books_selected = g.data['books_selected']
    g.features_list = g.data['features_list']
    g.up_voted = g.data['up_voted']
    g.down_voted = g.data['down_voted']
    g.books_returned = g.data['books_returned']
    print g.data
    print g.books_selected
    print g.features_list
    print g.up_voted
    print g.down_voted
    print g.books_returned
    g.Recommend = Recommend(user=g.user, db=db, Read=Read, Book=Book,
                            book_data=book_data, ipca_model=ipca_model, 
                            dict_vectorizer_fit=dict_vectorizer_fit, 
                            n_collab_returned=1000)
    g.recommended_books = g.Recommend.recommend_books(books_selected=g.books_selected, 
                                                      features_list=g.features_list, 
                                                      books_returned=g.books_returned)
    rec_data = {"recommendations": g.recommended_books}
    print rec_data
    return jsonify(rec_data)

         
