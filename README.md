Hello!

This web-app is still under construction, but check out the demo [here] (bit.ly/db-book-recommender)

The goal of this app is to create a book recommender that allows users to mix and match books they have read, as well as specific genres and topics. Most book recommenders suggest books based on your whole library, or all the books of a specific genre, when most of the time, genres are simply too broad of a category. By allowing users to choose the specific books off which to base the recommendation, they can adjust their results. Lastly, allowing users to up-vote and down-vote recommendations will add supervision to the learning, and impprove model in real-time. 

My method has been to combine collaborative filtering (Singular Value Decomposition, Principal Component Analysis) with 
content-similarity (K-Nearest Neighbors) and user up-voting/down-voting (Random Forest, Logistic Regression).

Stay tuned for the finished product!



# Bookology Book Recommender Web-App Overview

An app that allows user's to recieve book recommendations by inputing their own custom combination of books and features. The web app is built on flask and is configured to use an SQLite database, with Alembic for the migrations. Login and registration is included, along with social login (google and facebook) options. 

The app's recommendations are delivered on a basis of collaborative and content-based filtering. To achieve the collaborative filtering, the ratings for 160,000 users and 50,000 books were processed using an SVD to extract the latent features. The recommendations are further filtered by mapping the keywords users associated a book using an unsupervised KNeighbors model to determine distance from the user's input. Lastly, books that are very popular among all users are penalized, allowing for greater specificity in the results. 


## 1. Clone the repository

```$ git clone https://github.com/dberger1989/Important_Political_Entities_Finder.git```

## 2. Setup

This code is portable across the following OS's: Linux distributions, Mac and Windows OS's. Scripts were written using Python 2.7 and have not been tested for portability to Python 3.X.

You are encouraged to use a python virtual environment using virtualenv and pip. 

```$ virtualenv venv```

### Install requirements:

```$ pip install -r requirements.txt```

#### Description of modules imported and application

* beautifulsoup4 - Beautiful Soup sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
* Flask - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
* httplib2 - A comprehensive HTTP client library, httplib2 supports many features left out of other HTTP libraries.
* itsdangerous - Various helpers to pass trusted data to untrusted environments and back
* Jinja2 - Jinja2 is a full featured template engine for Python. It has full unicode support, an optional integrated sandboxed execution environment, widely used and BSD licensed
* fuzzywuzzy - Fuzzy string matching in python
* MarkupSafe - Implements a XML/HTML/XHTML Markup safe string for Python
* nltk - NLTK is a leading platform for building Python programs to work with human language data
* numpy - NumPy is the fundamental package for scientific computing with Python
* python-dateutil - Extensions to the standard Python datetime module
* requests - An Apache2 Licensed HTTP library, written in Python, for human beings
* selenium - Selenium automates browsers. That's it! What you do with that power is entirely up to you. Primarily, it is for automating web applications for testing purposes, but is certainly not limited to just that.
* six - Python 2 and 3 compatibility utilities
* Werkzeug - Werkzeug is a WSGI utility library for Python
* wheel - A built-package format for Python
* Whoosh - Whoosh is a fast, featureful full-text indexing and searching library implemented in pure Python.


## 3. Specify Foreign Affairs login and password credentials 

#### If you have a Foreign Affairs magazine subscription
If you would have a subscription to Foreign Affairs magazine, you can put your username and password in the config.py file. 
Doing so will allow you to scrape as many articles as you please. 

You can specify how many articles to scrape in the config.py file. The default is set to 100. 

#### If you do not have a Foreign Affairs magazine subscription
If you don't have a subscription, you can still run the web-app. I have scraped 100 articles and preprocessed them. This way, you can skip the scraping and processing and go straight to running the web app on flask. To do this, skip to 
**Run the app without scraping new data**, in instruction #6. 

## 4. Install google's chromedriver

Install from the website below using the appropriate link for your system:
	
```
http://chromedriver.storage.googleapis.com/index.html?path=2.19/
```

Specify the path to the downloaded chromedriver in the config.py file.  


## 5. Install NLTK dependencies

```
$ python -m nltk.downloader all
```



## 6. Run Scraping, Analysis, and Visuzalization

#### Run the app without scraping new data:
To run the web app using the pre-built index and avoid scraping altogether, run:
```
$ python important_political_entities_finder/visualize/app.py 
```

or:
### Run the full application
Application can be run separately or all at once from a shell script.

#### To run each part separately:

```
$ python -m important_political_entities_finder.ingest.fa_scrape
$ python -m important_political_entities_finder.wrangle.parse_and_make_index
$ python important_political_entities_finder/visualize/app.py 
```

#### To run via shell script:

```$ source bin/important_political_entities_finder.sh```

## 7. Go to web app!

The Flask app should be visible at the following location: 

``` http://127.0.0.1:5000/ ```
