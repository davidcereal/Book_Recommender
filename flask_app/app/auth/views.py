from flask import render_template, redirect, request, url_for, flash 
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, SearchForm
from flask.ext.login import logout_user, login_required, current_user
from .. import db


@auth.route('/login', methods=['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.register.data:
        return redirect(url_for('auth.register'))
    if form.validate_on_submit():
        print 'validated!!!!!'
        user = User.query.filter_by(email=form.email.data).first()
        print 'user:'
        print user
        if user is not None and user.verify_password(form.password.data):
            print 'password verified!!!'
            login_user(user, form.remember_me.data)
            print 'logged in!!!!'
            #return redirect(request.args.get('next') 
            return redirect(url_for('main.search'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=LoginForm())


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
    if form.validate_on_submit():
        print 'validated!!!!!!!!'
        user = User(email=form.email.data,
                    first_name = form.first_name.data,
                    password = form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('auth.login'))
    print form.errors
    return render_template('auth/register.html', form=form)
    
