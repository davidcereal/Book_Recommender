class User_rec(object):
	def __init__(self):
		books_selected = []



class preprocessing(object):
	def __init__(self, user):
		self.user = user

	#------------------------------Collaborative Filtering--------------------------#

	def prepare_ratings_for_dv(book_ids, db):
	    """
	    Function to query the database for the ratings the user attributed to the books
	    submitted. Then place ratings and book ids into format for the dict vectorizer.

	    Args:
	    book_ids (list of ints): A list containing the ids of the books the end-user has selected.
	    db: Database of users, books, and ratings. 
	    
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

	def dv_transform_enduser_vector(dict_vectorizer_fit, ratings_list):
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

	def ipca_tranform_enduser_vector(ipca_model, enduser_vector):
	    """
	    Use IPCA model fit on full user data transform 
	    the user vector, to predict what he/she would have filled in for missing 
	    values.
	    """
	    ipca_result = ipca_model.transform(enduser_vector)
	    ## Transform back to vector with results
	    filled_ratings = ipca_model.inverse_transform(ipca_result)[0]
	    return filled_ratings

	def create_user_authors_list(book_ids, book_data):
		"""
		Creates a list of the authors of the books input by the user.
		Args:
		book_ids: List of the book ids from end-user input 
		book_data: Full book data
		"""
	    user_authors_list = []
	    for book_id in book_ids:
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



	 def collaborative_filtering_predict(book_ids, book_data, db, n_books_returned):
	 	"""
	 	With enduser input of books and ratings, predict ratings for unread books and
	 	return highest predicted books.

	 	Args:
	 	book_ids: A list of the books the end-user submitted
	 	book_data: Full book library data
	 	db: database with users, books, and ratings
	 	n_books_returned: The number of books to be returned

	 	Returns:
	 	top_n_book_ids: The top n books the end-user is predicted to rate highest. 
	 	"""

	 	## Format end-user ratings into a list of dicts for the dict vectorizer
		unique_user_ratings_list = prepare_ratings_for_dv(book_ids)


	    ## Transform end-user ratings into vector fit on full user matrix 
	    ## and store the book names for later
	    book_names, enduser_vector = dv_transform_enduser_vector(dict_vectorizer_fit, ratings_list)
	    
	    ## Transform user vector and predict ratings
	    filled_enduser_ratings = ipca_tranform_user_point(ipca_model, enduser_vector)
	    
	    ## Make a list of the authors of the books the end-user submitted 
	    user_authors_list = create_user_authors_list(book_ids, book_data)
	    
	    ## Return the books the end-user is most likely to rate highest
	    top_n_book_ids = return_top_n_books(filled_enduser_ratings, n_books_returned, book_names, book_data, user_authors_list)
	    return top_n_book_ids

	#-----------------------------Find Keyword Preference-----------------------#
	
	def create_book_keyword_ranking(book_ids, book_data):
	    """
	    Create a dictionary with the end-user's books as keys and keyword:n times mentioned
	    as values.
	    
	    Arguments
	    book_ids: the end-user's books off which to base recommendation
	    book_data: Full data of all books in library
	    
	    Returns
	    book_keyword_ranking_dict: a dictionary of books and their keywords and the ammount 
	    times the are mentioned in association with the book.
	    
	    """
	    book_keyword_ranking_dict = {}
	    for book_id in book_ids:
	        if book_data.has_key(book_id):
	            keyword_rankings = book_data[book_id]['keywords']
	            book_keyword_ranking_dict[book_id] = keyword_rankings
	    return book_keyword_ranking_dict
	        

	def user_keyword_preferences(book_ids, book_data):
	    
	    """
	    Take a list of book ids and make a dictionary of keywords as keys and how many 
	    times each keyword is shared between books as the value
	    
	    Args: a list of book ids
	    Returns: a counter dictionary of keywords and counts
	    """    
	    ## Make a dictionary of the top ranked keywords for each book
	    book_keyword_ranking_dict = create_book_keyword_ranking(book_ids, book_data)
	    desired_keywords = []
	    for book, keywords in book_keyword_ranking_dict.items():
	        for keyword, value in keywords.items():
	            desired_keywords.append(keyword)
	    user_keyword_preferences = Counter(desired_keywords)
	    ## return a dictionary of how many times a keyword is shared between books
	    ## This should be improved in the future with a weighting process. 
	    return user_keyword_preferences



	def make_user_ranking(keyword_preferences, features_list):
	    """
	    Makes a dictionary where the keys are the most-shared keywords and the values are the rankings for them.
	    A top ranking will also go to all the features the user specified in input
	    
	    Arguments
	    keyword_preferences: a dictionary of keywords and how often they appear in the user's
	    bookshelf
	    features_list: a list of features the user specified
	    
	    Returns
	    user_preference: a dictionary where the keys are keywords and the values are their ranking
	    
	    """
	    user_preference = {}
	    user_preference['user'] = {}
	    for i, keyword in enumerate(sorted(keyword_preferences.items(), key=lambda x : x[1], reverse=True)):
	        user_preference['user'][keyword[0]] = 20 - i
	    for feature in features_list:
	        user_preference['user'][feature] = 20
	    return user_preference

	def make_top_books_keyword_dict(top_books, book_data):
	    """
	    Turns list of top book_ids returned from ipca and creates a dictionary where:
	    {book:{keyword:rank}}
	    """
	    top_books_keyword_dict = {}
	    for book_id in top_books:
	        try:
	            keywords = book_data[book_id]['keywords']
	            top_books_keyword_dict[book_id] = keywords
	            for key in top_books_keyword_dict[book_id].keys():
	                top_books_keyword_dict[book_id][key] = 1
	        except: 
	            continue
	    return top_books_keyword_dict

	def remove_non_shared_keywords(top_books_keyword_dict, user_preference):
	    """
	    Remove keywords from top_books if not shared with user_preference
	    """

	    top_books_keyword_dict_1 = copy.deepcopy(top_books_keyword_dict)
	    for book_id in top_books_keyword_dict_1:
	        for keyword in top_books_keyword_dict_1[book_id]:
	            if keyword not in user_preference['user'].keys():
	                del top_books_keyword_dict[book_id][keyword]
	    return top_books_keyword_dict

	def keep_only_if_in_feature_list(top_books, features_list, book_data):

	    """
	    Only keep books if they share a keyword with the keywords in the features_list
	    """
	    revised_top_books = {}
	    for book_id in top_books:
	        for keyword in book_data[book_id]['keywords']:
	            if keyword in features_list:
	                revised_top_books[book_id] = book_data[book_id]['keywords']
	    return revised_top_books


	def make_book_sample_and_test_point(top_n_book_ids, user_preference):
	    """
	    Turn the data of books and their keyword rankings and turn them into a sample, while 
	    turning the user's preference into a point. 
	    
	    Arguments
	    book_keyword_ranking_dict: dictionary of books as keys and keyword:rank as value
	    user_preference: custom user preference based on user inmput
	    
	    Returns:
	    sample: df with the books as rows and keywords as columns and counts as values
	    point: series with keywords as columns and rank as values
	    
	    """
	    
	    df = pd.DataFrame.from_dict(top_n_book_ids, orient='index')
	    ## Make a dataframe of the custom book dict, to be appended to the user dataframe 
	    df_to_append = pd.DataFrame.from_dict(user_preference, orient='index') 

	    ## Combine the two dataframes. 
	    df1 = df.append(df_to_append)
	    df2 = df1.fillna(0)
	    books_df = df2.ix[:-1, :]
	    enduser_series = df2.ix[-1:, :]
	    return books_df, enduser_series


	def apply_book_similarity_filtering(book_ids, book_data):
		"""
		Function to take end-user submitted books, find the keywords that are shared
		most among them, and are highest ranked, to determine end-user's preference.
		composition. Then, find out which books are most similar in keyword ranking composition 
		to end-user's preference.

		Args:
		book_ids (list of ints): A list of book ids
		book_data: A dictionary of full book data

		Returns:
		recommended_books (list of ints): List of book ids of the recommended books
		"""

	    ## Determine which how many times keywords are shared among end-user's 
	    ## submitted books.
	    user_keyword_preferences = user_keyword_preferences(book_ids, book_data)

	    ## Create ranking based on how many times keywords are shared
	    user_preference = make_user_ranking(user_keyword_preferences, features_list)

	    ## Make a dict of keywords for top books and n times keyword mentioned
	    top_books_keyword_dict = make_top_books_keyword_dict(top_books, book_data)

	    ## Only keep those books sharing a keyword with end-users keywords
	    if len(features_list) >= 1:
	        top_books_keyword_dict = keep_only_if_in_feature_list(top_books_keyword_dict, features_list, book_data)

	    ## Create dataframe of all books and their keyword rankings as columns
	    ## Create a series of end-user's "ideal" book keyword rankings  
	    books_df, enduser_series = make_book_sample_and_test_point(top_books_keyword_dict, user_preference)
	    sample_size = len(books_df)

	    ## Define clasifier
	    book_neigh = NearestNeighbors(n_neighbors=sample_size, algorithm='brute', metric='matching')
	    
	    ## Fit on full book df
	    book_neigh.fit(books_df) 

	    ## Determine distance from neighbors
	    book_nearest_neighbors = book_neigh.kneighbors(enduser_series, return_distance=True)
	    

	    ## Put neighbors in list
	    neighbors = np.ndarray.tolist(book_nearest_neighbors[1])[0]

	    ## Find the sum of all neighbor distances (good for benchmarking)
	    #sum_distances = sum(np.ndarray.tolist(book_nearest_neighbors[0])[0])
	    #print 'sum_distances_initial'
	    #print sum_distances
	    
	    ## Return the id's for the books and place in a list
	    recommended_books = [books_df.iloc[neighbor].name for neighbor in neighbors if neighbor not in books_returned]

	    return recommended_books





		
