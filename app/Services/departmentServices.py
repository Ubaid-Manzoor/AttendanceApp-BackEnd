from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, make_response, Response
import datetime 
import jwt


class departmentServices():
    
    @staticmethod
    def add_department(departmentName):
        departments = db['departments']
        print({"name":departmentName})
        try:
            departments.insert_one({"name":departmentName})
            return make_response({
                "status": 200,
                "result": {
                    "status": 201,
                    "message": "department created"
                }
            })
        except WriteError as werror:
            return make_response({
                "status": 200,
                "result": {
                    "status": 400,
                    "message": werror._message
                }
            })
            
    
    @staticmethod
    def get_all_departments():
        departments = db['departments']
        
        return departments.find({})