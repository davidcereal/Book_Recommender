class User_rec(object):
	def __init__(self):
		books_selected = []



class preprocessing(object):
	def __init__(self, user):
		self.user = user
	
	def prepare_ratings_for_dv(book_ids):
	    """
	    Function to place ratings and book ids into format for the dict vectorizer.

	    Args:
	    book_ids (list of ints): A list containing the ids of the books the end-user has selected.
	    
	    Returns:
	    ratings_list (list of dicts): A list containing dictionaries where each dict is in the format book_id:rating. 
	    """
	    ratings_list = []
	    rating_dict= {}
	    for book_id in book_ids:
	    	rating = db.session.query(Read).filter_by(user_id=g.user.id, book_id=book_id).first()
	        rating_dict[book_id] = rating
	    rating_list.append(ratings_dict)
	    return rating_list

	def transform_user_point(dict_vectorizer_fit, ratings_list):
	    """
	    Use Dict Vecotrizer object fit on full users data to transform the end-user's ratings
	    data into vector with similar columns. 
	    
	    Args:
	    dict_vectorizer_fit: A dict vectorizer object fit on all user ratings
	    ratings_list (list of dicts): A list containing all end-user ratings in book_id:rating 
	    format.

	    Returns:
	    enduser_vector: A vector of the end-user's ratings fit to the structure of the full 
	    rating matrix.
	    
	    book_names: A list of the names of the books in the order of columns in the matrices 
	    """
	    enduser_vector = dict_vectorizer_fit.transform(ratings_list)
	    book_names = dict_vectorizer_fit.feature_names_
	    return book_names, enduser_vector

	def tranform_user_point_with_ipca(ipca_model, enduser_vector):
	    """
	    Use IPCA model fit on full user data transform 
	    the user vector, to predict what he/she would have filled in for missing 
	    values.
	    """
	    ipca_result = ipca_model.transform(enduser_vector)
	    ## Transform back to vector with results
	    filled_ratings = ipca_model.inverse_transform(ipca_result)[0]
	    return filled_ratings
		
