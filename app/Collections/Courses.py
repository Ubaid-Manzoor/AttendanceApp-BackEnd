from app import db
from pymongo import errors
from collections import OrderedDict


class Courses:
    @staticmethod
    def create():

        query = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["student_enrolled"],
                "properties":{
                    "name": {
                        "bsonType": "string",
                        "description": "course name must be a string"  
                    },
                    "teacherAssigned": {
                        "bsonType": "string",
                        "description": "teacher must be a string"
                    },
                    "department": {
                        "bsonType": "string",
                        "description": "department must be a string"
                    },
                    "student_enrolled":{
                        "bsonType": "array",
                        "description": "student_enrolled must be an array and is required",
                        "items":{
                            "bsonType": "object",
                            "required": ["roll_no","encoding"],
                            "properties":{
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
            db.command(OrderedDict({
                "create":"courses",
                "validator": query,
                "validationLevel": "strict",
                "validationAction": "error"
            }))
            print("Collection Created!!!")
            
        except errors.OperationFailure:
            print("Collection Already Exists!!!")

