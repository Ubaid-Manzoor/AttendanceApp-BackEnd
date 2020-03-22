from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, make_response, Response
import datetime 
import jwt


class courseServices():
    
    @staticmethod
    def get_all_courses():
        courses = db['courses']
        return courses.find()
    
    
    @staticmethod
    def courseExists(courseName,department):
        courses = db['courses']
        return courses.find_one({"name":courseName,"department":department})
        
    @staticmethod
    def add_course(courseData):
        courses = db['courses']
        courseData = {
                "name":courseData['courseName'],
                "teacherAssigned":courseData['teacherAssigned'],
                "department": courseData['department'],
                "student_enrolled":[]
            }
        responseData = {
            "status": 200,
            "result": {}
        }
        
        if(courseServices.courseExists(courseData['name'],courseData['department'])):
            responseData["result"] = {
                        "status":409,
                        "message": "course Already Exist"
                    }
        else:    
            try:
                courses.insert_one(courseData)
                responseData["result"]={
                            "status":201,
                            "message": "Course Create"
                        }
            except WriteError as werror:
                responseData["result"]={
                            "status":400,
                            "message": werror._message
                        }

        return make_response(responseData)