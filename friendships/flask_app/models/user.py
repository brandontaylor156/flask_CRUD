from flask_app.config.mysqlconnection import connectToMySQL
import re 
from pprint import pprint

DATABASE = 'friendships_schema'
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.friends = []

    @classmethod
    def select_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return User(result[0])

    @classmethod
    def select_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for result in results:
            users.append( User(result) )
        return users

    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (first_name, last_name) VALUES (%(first_name)s, %(last_name)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def select_friendships(cls, data):
        query = "SELECT * FROM users JOIN friendships ON users.id = friendships.user_id LEFT JOIN users AS friends ON friends.id = friendships.friend_id WHERE users.id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if (results):
            user_var = User(results[0])

            for result in results:
                friend_dict = {
                    'id': result['friends.id'], 
                    'first_name': result['friends.first_name'], 
                    'last_name': result['friends.last_name'],
                    'created_at': result['friends.created_at'], 
                    'updated_at': result['friends.updated_at']
                }
                
                user_var.friends.append(User(friend_dict))
            
        else:
            return False

        return user_var

    @classmethod
    def insert_friendship(cls, data):
        if data['user_id'] == data['friend_id']:
            return False

        query = "INSERT INTO friendships (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
    #     result = connectToMySQL(DATABASE).query_db(query, data)
    #     return result

    # @classmethod
    # def delete(cls, data):
    #     query = "DELETE FROM users WHERE id = %(id)s;"
    #     result = connectToMySQL(DATABASE).query_db(query, data)
    #     return result

        