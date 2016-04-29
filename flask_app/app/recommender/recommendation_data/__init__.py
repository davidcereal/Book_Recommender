import pickle

import os

scriptdir = os.path.dirname(os.path.abspath(__file__))

book_data_path = os.path.join(scriptdir, "engineered_book_data.pkl")
DV_fit_path = os.path.join(scriptdir, "DV_fit.pkl")
ipca_model_path = os.path.join(scriptdir, "ipca_model.pkl")

with open(book_data_path, 'r') as picklefile:
    book_data = pickle.load(picklefile)

with open(DV_fit_path, 'r') as picklefile:
    dict_vectorizer_fit = pickle.load(picklefile)

with open(ipca_model_path, 'r') as picklefile:
    ipca_model = pickle.load(picklefile)