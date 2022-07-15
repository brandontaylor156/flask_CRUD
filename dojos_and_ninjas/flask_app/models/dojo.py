from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja
from pprint import pprint

DATABASE = 'dojos_and_ninjas'
class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.ninjas = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL(DATABASE).query_db(query)
        dojos = []
        for result in results:
            dojos.append( Dojo(result) )
        return dojos

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    @classmethod
    def show_ninjas(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        dojo = Dojo(results[0])

        for result in results:
            ninja_dict = {
                'id': result['ninjas.id'], 
                'first_name': result['first_name'], 
                'last_name': result['last_name'],
                'age': result['age'],
                'dojo_id': result['dojo_id'], 
                'created_at': result['ninjas.created_at'], 
                'updated_at': result['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(ninja_dict))
        return dojo
        

        
        

        


        

        

