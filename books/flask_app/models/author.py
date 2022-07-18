from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
from flask_app import flash
import re, pprint

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE = 'books_schema'
class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL(DATABASE).query_db(query)
        authors = []
        for result in results:
            authors.append( Author(result) )
        return authors

    @classmethod
    def insert_one(cls, data):
        query = "INSERT INTO authors (first_name, last_name) VALUES (%(first_name)s, %(last_name)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    @classmethod
    def get_all_relationships(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        author = Author(results[0])

        for result in results:
            book_dict = {
                'id': result['books.id'], 
                'title': result['title'], 
                'num_of_pages': result['num_of_pages'],
                'created_at': result['books.created_at'], 
                'updated_at': result['books.updated_at']
            }
            author.books.append(book.Book(book_dict))
        return author
    
    @classmethod
    def save_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    

        


        

        

