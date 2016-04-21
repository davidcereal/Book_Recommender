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

	def create_user_authors_list(id_list, book_data):
		"""
		Creates a list of the authors of the books input by the user.
		Args:
		id_list: List of the book ids of the books input 
		book_data: Full book data
		"""
	    user_authors_list = []
	    for book_id in id_list:
	        if book_data.has_key(book_id):
	            author = book_data[book_id]['author']
	            user_authors_list.append(author)
	    return user_authors_list

	def return_top_n_books(filled_ratings, n_results, book_names, book_data, read_authors_list):
	    """
	    Return the top n number of books from the ipca model results.

	    Args:
	    filled_ratings: The end-user vector with all book ratings predicted
	    n_results: The number of results to return (most strong predictions delivered first)
	    book_names: The names of the books, in order of vector columns.
	    book_data: Full book data


		Returns:
		top_n_book_ids: A list of the ids of the top book suggestions    
		"""
	    ## Attach book names to the results
	    results = sorted(zip(book_names, filled_user_ratings), key = lambda x: x[1], reverse=True)
	    top_n_book_ids = []
	    for item in results[:n]:
	        book_id = item[0]
	        if book_data.has_key(book_id):
	            if book_data[book_id].has_key('author'):
	            	if book_data[book_id]['author'] not in read_authors_list:
	                	top_n_book_ids.append(book_id)
	    return top_n_book_ids

		
