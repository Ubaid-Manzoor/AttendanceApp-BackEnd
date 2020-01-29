from app import db 
from pymongo import errors

class Attendance:

    @staticmethod:
    def create():
        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "properties":{
                    "_id":{
                        "bsonType": "string",
                        "description": "_id must be a string"
                    }
                }
            }
        }

        try:
            db.command({
                "create": "attendance",
                "validator": query,
                "validationLevel": "strict",
                "validationAction": "error"
            })
        except errors.OperationFailure:
            print("Collection Already Exists!!!")

