from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired, URL
from wtforms import ValidationError
from ..models import User
from flask.ext.bcrypt import Bcrypt
from flask.ext.openid import OpenID

bcrypt = Bcrypt()
oid = OpenID()


class OpenIDForm(Form):
    openid = StringField('OpenID URL', [DataRequired(), URL()])

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email(message='Valid email address required')])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Keep me logged in')
    submit_login = SubmitField('Log In')
    register = SubmitField('Sign Up')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email(message='Valid email address required')])
    name = StringField('Name', validators= [Required(), Length(1, 64)])
    #last_name = String(Field('Last Name'), validators= [Length(1, 64)])
    password1 = PasswordField('Password', validators=[Required(), 
                                                    Length(min=8, message='Password must be at least 8 characters long')])
    password2 = PasswordField('Confirm password', validators=[Required(), 
                                                            EqualTo('password1', message='Passwords must match.')])
    recaptcha = RecaptchaField()
    register = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('That email address is already registered.')

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])