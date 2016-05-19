from datetime import datetime
from flask import render_template, session, redirect, url_for, g, request, jsonify, send_from_directory
from . import main
from .. import db
from ..models import User, Book, Read
from ..auth.forms import LoginForm, RegistrationForm, SearchForm
from .. import auth
from flask.ext.login import login_required, current_user
from flask_app.config import Config
from flask_wtf.csrf import CsrfProtect
import os
import pickle


@main.route('/', methods=['GET', 'POST'])
@login_required 
def index():
    return redirect(url_for('recommender.recommendations'))


@main.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.search_form = SearchForm()
    #g.locale = get_locale()

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.search.data:
        session['query'] = g.search_form.search.data
        return redirect(url_for('main.search_results', query=g.search_form.search.data))
    elif session.get('query'):
        return redirect(url_for('main.search_results', query=session.get('query')))
    return render_template('search.html', form=form)


@main.route('/search_results/<query>', methods=['GET', 'POST'])
@login_required
def search_results(query):
    results = Book.query.whoosh_search(query, Config.MAX_SEARCH_RESULTS).all()
    for book in results:
        if book in current_user.books_read:
            print True
    return render_template('search_results.html',
                           query=query,
                           results=results,
                           db=db,
                           Read=Read)

@main.route('/rating', methods=['GET', 'POST'])
@login_required
def rating():
    data = request.json
    rating = data['rating'][1]
    web_id = data['rating'][0]

    book = db.session.query(Book).filter(Book.web_id==data['rating'][0]).first()

    book_read = Read(user=g.user.id, book=book, rating=rating)
    print 'book read add'
    print book_read
    db.session.add(book_read)
    db.session.commit()
    print 'book {} added'.format(book.title)
    book_rating = {"book rated": [book.title]}
    return jsonify(book_rating)


@main.route('/library', methods=['GET', 'POST'])
@login_required
def library():
    return render_template('library.html', current_user = g.user, db=db, Book=Book)


@main.route('/delete_read', methods=['GET', 'POST'])
@login_required
def delete_read():
    data = request.json
    #print "data:{}".format(data)
    book_id = data['book_info'][0]
    book = db.session.query(Book).filter(Book.web_id==book_id).first()
    read_record = db.session.query(Read).filter_by(book=book, user_id=g.user.id).first()
    print 'read record delete:'
    print read_record
    db.session.delete(read_record)
    db.session.commit()
    print 'book {} deleted'.format(book.title)
    book_deleted = {'book deleted': read_record.book_id}
    return jsonify(book_deleted)

@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


