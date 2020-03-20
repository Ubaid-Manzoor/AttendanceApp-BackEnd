from app import db
from pymongo import errors
from collections import OrderedDict 

class Users:

    @staticmethod
    def create():
        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['password','role'],
                "properties": {
                    "_id": {
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
            print("User Collection  Creation Failure !!!")