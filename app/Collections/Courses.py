from app import db
from pymongo import errors

class Courses:
    @staticmethod
    def create():

        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["student_enrolled"],
                "properties":{
                    "_id":{
                        "bsonType": "string",
                        "description": "_id must be a string"
                    },
                    "student_enrolled":{
                        "bsonType": "array",
                        "description": "student_enrolled must be an array and is required",
                        "items":{
                            "bsonType": "object",
                            "required": ["name","roll","encoding"],
                            "properties":{
                                "name": {
                                    "bsonType": "string",
                                    "description": "name must be a string and is required"
                                },
                                "roll_no": {
                                    "bsonType": "string",
                                    "description": "roll must be a string and is required"
                                },
                                "encoding": {
                                    "bsonType": "array",
                                    "description": "encoding must be an array and is required"
                                }
                            }
                        }
                    }
                }
            }                
        }
        try:
            db.command({
                "create":"courses",
                "validator": query,
                "validationLevel": "strict",
                "validationAction": "error"
            })
            print("Collection Created!!!")
        except errors.OperationFailure:
            print("Collection Already Exists!!!")

