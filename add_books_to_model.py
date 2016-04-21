from app.db import Book as Book

import pickle
with open('/Users/David/icloud/ds/scrap/book_data_title_space_removed.pkl', 'r') as picklefile:
	book_data = pickle.load(picklefile)

print Book.__table__

db.create_all()

def add_books_to_db(book_data, db, Book):
	'''
	Function to add books and their data to database
	'''
	for book in book_data.keys()[:50]:
		if book_data[book].has_key('title') and book_data[book].has_key('author') \
			and book_data[book].has_key('description') and book_data[book].has_key('keywords'):
			title = book_data[book]['title']
			author = book_data[book]['author']
			web_id = book
			description = book_data[book]['description']
			keywords_dict = book_data[book]['keywords']
			book_entry = Book(title=title, author=author, web_id=web_id, description=description)
			db.session.add(book_entry)
			db.session.commit()
			for keyword in keywords_dict:
				keyword_label = keyword
				keyword_weight = keywords_dict[keyword]
				keyword_entry = Keyword(keyword_label=keyword_label)
				db.session.add(keyword_entry)
				db.session.commit()
				book_keyword_entry = Book_Keyword(keyword_weight=keyword_weight, book=book_entry, keyword=keyword_entry)
				db.session.add(book_keyword_entry)
				db.session.commit()

add_books_to_db(book_data, db, Book)

if __name__ == "__main__":
	run main()
