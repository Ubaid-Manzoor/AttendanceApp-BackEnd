from app import db
from pymongo import errors 
from collections import OrderedDict 


class Departments:
    
    @staticmethod 
    def create():
        
        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['name'],
                "description": "department must be an object",
                "properties":{
                    "name": {
                        "bsonType": "string",
                        "description": "name must be a string"
                    }
                    
                }
            }
        }
        
        try:
            db.command(OrderedDict({
                "create": "departments",
                "validator": query,
                "validationLevel" : "strict",
                "validationAction" : "error"
            }))
            print("Department Collection Created !!!")
            
        except errors.OperationFailure:
            print("Collection Already Exists")