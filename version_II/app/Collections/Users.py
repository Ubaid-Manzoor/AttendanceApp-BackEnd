from app import db
from pymongo import errors
from collections import OrderedDict 

class Users:

    @staticmethod
    def create():
        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['name','password','role'],
                "properties": {
                    "_id": {
                        "bsonType": "string",
                        "description": "must be a string"
                    },
                    "name": {
                        "bsonType": "string",
                        "description": "must be a string"
                    },
                    "department": {
                        "bsonType": "string",
                        "description": "must be a string"
                    },
                    "password":{
                        "bsonType": "string",
                        "description": "must be a string"
                    },
                    "role":{
                        "bsonType": "string",
                        "description": "must be a string"
                    },
                    "confirmed": {
                        "bsonType": "bool",
                        "description": "must be a boolean"
                    }
                }
            }
        }

        try:
            db.command(OrderedDict({
                "create": "users",
                "validator": query,
                "validationLevel": "strict",
                "validationAction": "error"
            }))
            print("User Collection Created!!")

        except errors.OperationFailure as error:
            print(error)