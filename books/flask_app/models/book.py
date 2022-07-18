from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
from flask_app import flash
import re, pprint

DATABASE = 'books_schema'
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(DATABASE).query_db(query)
        books = []
        for result in results:
            books.append( Book(result) )
        return books

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def save_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return Book(result[0])

    @classmethod
    def get_all_relationships(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        book = Book(results[0])

        for result in results:
            author_dict = {
                'id': result['authors.id'], 
                'first_name': result['first_name'], 
                'last_name': result['last_name'],
                'created_at': result['authors.created_at'], 
                'updated_at': result['authors.updated_at']
            }
            book.authors.append(author.Author(author_dict))
        return book
    

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

        
        

