from flask import render_template, session, redirect, url_for, g, request, jsonify
from . import recommender
from .. import db
from ..models import User, Book, Read
from flask_app.config import Config, config
from flask.ext.login import login_required, current_user
from flask_wtf.csrf import CsrfProtect
from recommend import Recommend, format_keywords_for_d3, get_book_info
import recommender_data
from recommender_data import book_data, dict_vectorizer_fit, ipca_model
import os




@recommender.before_request
def before_request():
    g.user = current_user


@recommender.route('/recommendations', methods=['GET', 'POST']) 
@login_required
def recommendations():
    books_read = []
    for book_read in current_user.books_read:
        book = db.session.query(Book).filter_by(id=book_read.book_id).first()
        web_id = book.web_id
        books_read.append(web_id)
    return render_template('recommendations.html', current_user=g.user, db=db, Book=Book, books_read=books_read)

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
    g.books_read = g.data['books_read'] 

    for book in g.books_read:
        g.books_returned.append(str(book))


    g.Recommend = Recommend(user=g.user, db=db, Read=Read, Book=Book,
                            book_data=book_data, ipca_model=ipca_model, 
                            dict_vectorizer_fit=dict_vectorizer_fit)
    g.recommended_books = g.Recommend.recommend_books(books_selected=g.books_selected, 
                                                      features_list=g.features_list, 
                                                      books_returned=g.books_returned,
                                                      up_votes=g.up_voted, 
                                                      down_votes=g.down_voted,
                                                      n_collab_returned=1000)
    rec_data = {"recommendations": g.recommended_books}
    return jsonify(rec_data)

# Get user books and features input and return recommendations 
@recommender.route("/recommendations/results/visualize", methods=["POST"])
@login_required
def keywords_to_d3():
    g.data = request.json
    g.book_id = g.data["book_id"][0]
    g.book_keywords = book_data[g.book_id]['keywords']
    g.d3_keywords = format_keywords_for_d3(g.book_keywords)
    g.book_info = get_book_info(g.book_id, book_data)
    g.results = {"book_info":g.book_info, "d3_info": {'name': 'flare', "children": [{'name': 'cluster', 'children': g.d3_keywords}]}}
    return jsonify(g.results)

         
