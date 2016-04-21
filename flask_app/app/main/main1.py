from flask import Flask, render_template, session, redirect, url_for, flash

from flask.ext.sqlalchemy import SQLAlchemy
import os

class LoginForm(Form):
	username = StringField('username', validators=[Required()]) 
	password = PasswordField('password', validators=[Required()])
	submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Encryption_String'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)






@app.route('/', methods=['GET', 'POST']) 
def index():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
			if user is None:
				username = User(username = form.username.data)
				db.session.add(user)
				session['known'] = False
			else:
				session['known'] = True
			session['username'] = form.username.data
			form.username.data = ''
			return redirect(url_for('index'))
		return render_template('index.html',
								form = form, 
								username= session.get('username'),
								known = session.get('known', False))

@app.route('/user/<name>') 
def user(name):
    return render_template('user.html', name=name)



if __name__ == '__main__': app.run(debug=True)
