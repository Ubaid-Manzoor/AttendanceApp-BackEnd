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
                    "attendance": {
                        "bsonType": "array",
                        "description" : "attendance should me an array of objects",
                        "items": {
                            "bsonType": "object",
                            "required": ["date","attendance_on_date"],
                            "properties": {
                                "date": {
                                    "bsonType": "date",
                                    "description": "date must be a date object"
                                },
                                "attedance_on_date":{
                                    "bsonType": "array",
                                    "description": "attendance_on_date should be a of attendances",
                                    "items": {
                                        "bsonType": "object",
                                        "required": ["roll_no","status"],
                                        "properties": {
                                            "roll_no": {
                                                "bsonType" : "string",
                                                "description": "roll_no should be a string"
                                            },
                                            "status": {
                                                "bsonType": "bool",
                                                "description": "status should be a boolean"
                                            }
                                        }
                                    }
                                }
                            }
                        }
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
            
        except errors.OperationFailure as error:
            print(error)

