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

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None


    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()

        if user is None:
            self.email.errors.append('Email address does not belong to registered user')
            return False

        if not user.verify_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


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

    


'''    def validate(self):
        print 'validate user accessed'
        user = User.query.filter_by(email=field.data).first()
        if user is not None and user.verify_password(field.data):
            print 'invalid user!'
            raise ValidationError('Invalid username/password combination')'''

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])