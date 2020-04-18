from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, Response
import datetime 
import jwt


class departmentServices():
    
    @staticmethod
    def add_department(name):
        departments = db['departments']
        print({"name":name})
        
        filter = {
            "name": name
        }
        if(not departments.find_one(filter)):
            try:
                departments.insert_one({"name":name})
                return jsonify({
                    "status": 200,
                    "result": {
                        "status": 201,
                        "message": "department created"
                    }
                })
            except WriteError as werror:
                return jsonify({
                    "status": 200,
                    "result": {
                        "status": 400,
                        "message": werror._message
                    }
                })
        else:
            return jsonify({
                "status": 200,
                "result": {
                    "status": 409,
                    "message": "Department Already Exists"
                }
            })
                
    
    @staticmethod
    def get_all_departments():
        departments = db['departments']
        
        return departments.find({})