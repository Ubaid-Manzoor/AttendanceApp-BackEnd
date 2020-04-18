from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, Response
import datetime 
import jwt


class studentServices():
    @staticmethod
    def enroll_student(course_to_enroll,student_data):
        courses = db['courses']

        response = {
            "name": course_to_enroll,
            "status": 200,
            "result": {
                
            }
        }
        try:
            roll_no = student_data.get('roll_no')
            studentEnrolled =  \
                courses.find_one({"name": course_to_enroll,
                              "student_enrolled": {"$elemMatch":{"roll_no":roll_no} } 
                            })
            # print(studentEnrolled)
            if(not studentEnrolled):
                courses.update({"name":course_to_enroll},{"$push":{"student_enrolled":student_data}})
                response.update({
                    "result": {
                        "status": 201,
                        "message": "Student Enrolled!!!"
                    }
                })
            else:
                response.update({
                    "result": {
                        "status": 409,
                        "message": "Already Enrolled"
                    }
                })

        except WriteError as werror:
            response.update({
                "result": {
                    "status": 400,
                    "message": werror._message
                }
            })
            
        return response
    
    @staticmethod
    def get_all_students(filters, projection):
        users = db['users']
        if not filters:
            filters = ({
                "role": "student"
            })
            
        else:
            filters.update({
                "role": "student"
            })
        
        return users.find(filters, projection)
    
    
    
    @staticmethod
    def update_student(studentToUpdate, _toSet):
        users = db['users']
        
        _filter = {
            "_id": studentToUpdate
        }
        
        try:
            users.update_one(_filter,{'$set': _toSet})
            return jsonify({
                "status":200
            })
        except:
            return jsonify({
                "status": 400
            })


    @staticmethod
    def get_all_students_enrolled(name:str, department:str, semester:int):
        courses = db['courses']
        return courses.find_one({"name":name,"department": department, "semester":semester})['student_enrolled']