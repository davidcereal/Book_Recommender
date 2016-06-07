# NextReads Book Recommender Web-App Overview
NextReads is a web-app that allows users to get recommendations by mixing and matching books they have read, as well as specific genres and topics. Most book recommenders suggest books based on your whole library, or all the books of a specific genre, when most of the time, genres are simply too broad of a category. By allowing users to choose the specific books off which to base the recommendation, they can adjust their results in real time. Lastly, allowing users to up-vote and down-vote recommendations will add supervision to the learning, and impprove their recommendations in real time.


The app's recommendations are delivered on a basis of collaborative and content-based filtering. To achieve the collaborative filtering, the ratings for 160,000 users and 50,000 books were processed using an SVD to extract the latent features. The recommendations are further filtered by mapping the keywords users associated a book using a KNeighbors model to determine distance from the user's input. Lastly, books that are very popular among all users are penalized, allowing for greater specificity in the results. Users are given the option of up-voting and down-voting the suggestions, and this feedback updates the collaborative filtering output. 


## Clone the repository

```$ git clone https://github.com/dberger1989/Book_Recommender.git```

## Setup

This code is portable across the following OS's: Linux distributions, Mac and Windows OS's. Scripts were written using Python 2.7 and have not been tested for portability to Python 3.X.

You are encouraged to use a python virtual environment using virtualenv and pip. 

```$ virtualenv venv```

### Install requirements:

```$ pip install -r requirements.txt```

#### Description of modules imported and application


* alembic==0.8.6
* bcrypt==2.0.0
* blinker==1.4
* cffi==1.6.0
* Flask==0.10.1 - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
* Flask-Bcrypt==0.7.1
* Flask-Login==0.3.2
* Flask-Migrate==1.8.0
* Flask-Moment==0.5.1
* Flask-OAuth==0.12
* Flask-OpenID==1.2.5
* Flask-Script==2.0.5
* Flask-SQLAlchemy==2.1
* Flask-WhooshAlchemy==0.56
* Flask-WTF==0.12
* httplib2==0.9.2 - A comprehensive HTTP client library, httplib2 supports many features left out of other HTTP libraries.
* itsdangerous==0.24 - Various helpers to pass trusted data to untrusted environments and back
* Jinja2==2.8
* Mako==1.0.4
* MarkupSafe==0.23 - Implements a XML/HTML/XHTML Markup safe string for Python
* numpy==1.11.0 - NumPy is the fundamental package for scientific computing with Python
* oauth2==1.9.0.post1
* pandas==0.18.1
* pycparser==2.14
* python-dateutil==2.5.3
* python-editor==1.0
* python-openid==2.2.5
* pytz==2016.4
* scikit-learn==0.17.1
* scipy==0.17.0
* six==1.10.0 - Python 2 and 3 compatibility utilities
* SQLAlchemy==1.0.12
* Werkzeug==0.11.9 - Werkzeug is a WSGI utility library for Python
* Whoosh==2.7.4 - Whoosh is a fast, featureful full-text indexing and searching library implemented in pure Python.
* WTForms==2.1

## App structure

### Blueprints

This app utilizes 3 blueprints created upon instantiation:
* main - handles the basic views of the site
* auth - handles views of the site relevant to registartion and login
* recommender - handles views relevant to generating recommendations

### Static and Large Files

Because of Elastic Beanstalk's upload limit of 512mb, the static files and the recommendation models are accessed by connecting to an S3 bucket. 

### SQL

* The database for the website is stored on an Amazon RDS server implementing PostgreSQL 






