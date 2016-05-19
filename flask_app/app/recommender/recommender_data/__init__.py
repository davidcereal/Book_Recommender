
import pickle

import os, sys
import boto3 

from flask_app.config import Config
 

scriptdir = os.path.dirname(os.path.abspath(__file__))



#scriptdir = '/home/ec2-user/flask_app_data/recommender_data/'

book_data_path = os.path.join(scriptdir, "engineered_book_data.pkl")
#DV_fit_path = os.path.join(scriptdir, "DV_fit.pkl")
DV_fit_path = os.path.join(scriptdir, "dict_vectorizer_fit_160k_top_50k_books_duplicates_removed_user_data.pkl")

#ipca_model_path = os.path.join(scriptdir, "ipca_model.pkl")
#ipca_model_path = os.path.join(scriptdir, "ipca_37k_nc150_bs500.pkl")
#ipca_model_path = os.path.join(scriptdir, "ipca_fillmean_37k_nc100_bs500.pkl")
ipca_model_path = os.path.join(scriptdir, "ipca_160k_nc50_bs500.pkl")


#conn = boto.connect_s3(Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY)

s3 = boto3.client('s3')

s3.download_file("brstatic", "static/recommender_data/dict_vectorizer_fit_160k_top_50k_books_duplicates_removed_user_data.pkl", DV_fit_path)
s3.download_file("brstatic", "static/recommender_data/engineered_book_data.pkl", book_data_path)
s3.download_file("brstatic", "static/recommender_data/ipca_160k_nc50_bs500.pkl", ipca_model_path)




features_list = []

with open(book_data_path, 'r') as picklefile:
    book_data = pickle.load(picklefile)

with open(DV_fit_path, 'r') as picklefile:
    dict_vectorizer_fit = pickle.load(picklefile)

with open(ipca_model_path, 'r') as picklefile:
    ipca_model = pickle.load(picklefile)