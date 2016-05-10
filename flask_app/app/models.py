from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask.ext.login import UserMixin
import flask.ext.whooshalchemy

class Read(db.Model):
    __tablename__ = 'reads'
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True, index=True)
    rating = db.Column(db.Integer, index=True)
    book = db.relationship("Book", back_populates='users')
    user = db.relationship("User", back_populates='books_read')


        

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), index=True)
    social_id = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    books_read = db.relationship('Read', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class Book(db.Model):
    __tablename__ = 'books'
    __searchable__ = ['title', 'author']  
    id = db.Column(db.Integer, primary_key=True, index=True)
    web_id = db.Column(db.Integer, unique=True, index=True)
    title = db.Column(db.String, index=True)
    author = db.Column(db.String, index=True)
    publication_date = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    users = db.relationship('Read', back_populates='book') 
    keywords = db.relationship('Book_keyword', back_populates='book')

    def __repr__(self):
        return '<Book %r>' % self.title

class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True, index=True)
    keyword_label = db.Column(db.String, index=True)
    books = db.relationship('Book_keyword', back_populates='keyword')

    def __repr__(self):
        return '<Keyword %r>' % self.keyword_label

class Book_keyword(db.Model):
    __tablename__ = 'book_keywords'
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True, index=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'), primary_key=True, index=True)
    keyword_weight = db.Column(db.Integer, index=True)
    book = db.relationship('Book', back_populates='keywords') 
    keyword = db.relationship('Keyword', back_populates='books') 



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

