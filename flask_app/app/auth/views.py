from flask import render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user
from . import auth

from config import Config

from ..models import User
from .forms import LoginForm, RegistrationForm, SearchForm, OpenIDForm
from flask.ext.login import logout_user, login_required, current_user, login_user
from .. import db

from flask.ext.bcrypt import Bcrypt
from flask.ext.openid import OpenID
from flask_oauth import OAuth


bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=Config.FB_CONSUMER_KEY,
    consumer_secret=Config.FB_CONSUMER_SECRET,
    request_token_params={'scope': 'email'})

google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    request_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params={'grant_type': 'authorization_code'},
    access_token_method='POST',
    consumer_key=Config.GOOGLE_CLIENT_ID,
    consumer_secret=Config.GOOGLE_CLIENT_SECRET,
    request_token_params={'scope': 'openid email',
                        'response_type': 'code'})





@google.tokengetter
def get_google_oauth_token():
    return session.get('google_oauth_token')

@auth.route('/google')
def google_login():
    form = LoginForm()
    return google.authorize(
        callback=url_for(
            '.google_authorized',
            next=None,
            _external=True))


@auth.route('/google/authorized')
@google.authorized_handler
def google_authorized(resp):
    form = LoginForm()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if session.has_key('google_oauth_tokens'):
        del session['google_oauth_tokens']
    session['google_oauth_token'] = (resp['access_token'], '')
    me = google.get("https://www.googleapis.com/oauth2/v2/userinfo")
    print me.data
    user = db.session.query(User).filter_by(
        social_id=me.data['id']).first()

    if not user:
        user = User(social_id=me.data['id'], email=me.data['email'], name=me.data['given_name'])
        db.session.add(user)
        db.session.commit()

    login_user(user, form.remember_me.data)
    flash("You have been logged in.", category="success")

    return redirect(url_for('recommender.recommendations'))






@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth_token')



@auth.route('/login', methods=['GET', 'POST']) 
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()
    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['email'],
            #ask_for_optional=['first_name']
            )
    if form.register.data:
        return redirect(url_for('auth.register'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            #return redirect(request.args.get('next') 
            flash("You have been logged in.", category="success")
            return redirect(url_for('recommender.recommendations'))
        flash('Invalid username or password.')

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    return render_template('auth/login.html', form=LoginForm(), openid_form=openid_form)


@auth.route('/facebook')
def facebook_login():
    form = LoginForm()
    return facebook.authorize(
        callback=url_for(
            '.facebook_authorized',
            next=url_for('recommender.recommendations'),
            _external=True, 
            form=form
        )
    )



@auth.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    form = LoginForm()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['facebook_oauth_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    print me.data
    user = db.session.query(User).filter_by(
        social_id=me.data['id']).first()

    if not user:
        user = User(social_id=me.data['id'], name=me.data['name'])
        db.session.add(user)
        db.session.commit()

    login_user(user, form.remember_me.data)
    flash("You have been logged in.", category="success")

    return redirect(url_for('recommender.recommendations'))






@auth.route('/logout') 
@login_required
def logout():
    logout_user()
    flash('You have been logged out.') 
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    print 'accessed the register route'
    form = RegistrationForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['email'],
            #ask_for_optional=['first_name']
        )

    if form.validate_on_submit():
        print 'validated!!!!!!!!'
        user = User(email=form.email.data,
                    name = form.name.data,
                    password = form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('recommender.recommendations'))
    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")


    print form.errors
    return render_template('auth/register.html', form=form, openid_form=openid_form)
    
