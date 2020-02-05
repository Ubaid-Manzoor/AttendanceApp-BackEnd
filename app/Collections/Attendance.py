from app import db 
from pymongo import errors
from collections import OrderedDict

class Attendance:

    @staticmethod:
    def create():
        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["attendance"]
                "properties":{
                    "_id":{
                        "bsonType": "string",
                        "description": "_id must be a string"
                    },
                    "attendance":{
                        "bsonType": "object",
                        "description": "attendance must be an object"
                    }
                }
            }
        }

        

        try:
            db.command(OrderedDict({
                "create": "attendance",
                "validator": query,
                "validationLevel": "strict",
                "validationAction": "error"
            }))
        except errors.OperationFailure as FailureError:
            print(FailureError)

