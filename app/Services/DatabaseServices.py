#CRUD Related Services
from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, make_response, Response
import datetime 
import jwt

class DatabaseServices():

    @staticmethod
    def initiate_database():
        ##Create Courses Collection
        Courses.create()

        ##Create Users Collection
        Users.create()
        
        ##Create Department Collection
        Departments.create()
        
    @staticmethod
    def get_all_students_enrolled(course_name:str):
        courses = db['courses']
        return courses.find_one({"_id":course_name})
    
    @staticmethod
    def get_all_courses():
        courses = db['courses']
        return courses.find()

    @staticmethod
    def get_encodings(class_name):
        pass 


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
        
        if(DatabaseServices.courseExists(courseData['name'],courseData['department'])):
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
    @staticmethod
    def enroll_student(course_to_enroll,student_data):
        
        courses = db['courses']

        ## Initializing Message and status for response
        # print({"_id":course_to_enroll},{"$push":{"student_enrolled":student_data}})
        message = ""
        status = 201
        try:
            courses.update({"_id":course_to_enroll},{"$push":{"student_enrolled":student_data}})
            message = "Students Enrolled !"
        except WriteError as werror:
            message = werror._message 
            status = 400
        
        return jsonify({     

            "status": status,
            "message": message
        })
        
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
    def mark_present(student_roll):
        pass 

    @staticmethod
    def mark_absent(student_roll):
        pass

        
    @staticmethod
    def usernameExists(username:str):
        users = db['users']
        return users.find_one({"_id":username})

    @staticmethod
    def signup(user:dict):
        users = db['users']
        
        userData = {
            "_id": user['username'],
            "name": user['name'],
            "department": user['department'],
            "password": user['password'],
            "role": user['role'],
            "confirmed": user['confirmed'] if user['confirmed'] else False
        }
        if(user['role'] == "student"):
            userData['semester'] = user['semester']


        if(DatabaseServices.usernameExists(user['username'])):
            response = {
                "status": 200,
                "result": {
                    "status": 409,
                    "message": "username already exists!"
                }
            }
        else:
            try:
                users.insert_one(userData)
                response = {
                    "status": 200,
                    "result" : {
                        "status": 201,
                        "message": "user created"
                    }
                }
            except WriteError:
                response = {
                    "status": 200,
                    "result": {
                        "status": 422,
                        "message": "wrong input by user"
                    }
                }
    
        return jsonify(response)


    @staticmethod
    def check_user(username:str,password:str):
        Users = db['users']
        
        return Users.find_one({"_id": username,"password":password})

    @staticmethod
    def get_user(username:str):
        Users = db['users']
        
        return Users.find_one({"_id":username})
    
    @staticmethod
    def login(username,password):
        user = DatabaseServices.check_user(username,password)
        
        if(user and user['role'] != "admin" and (not user['confirmed'])):
            responseData = {
                "status": 200,
                "result": {
                    "status":403,
                    "message": "Confirmation is Pending"
                }
            }
            response = make_response(responseData)
        elif(user):
            # jwToken = jwt.encode(user,username).decode()
            responseData = {
                "status":200,
                "result":{
                    "data":{
                        "username":username,
                        "role":user['role']
                        },
                    "status": 200,
                    "message": "User is Logged In"
                }
            }
            response = make_response(responseData)
            

        else:
            responseData = {
                "status": 200,
                "result":{
                    "status": 401,
                    "message": "username or password is wrong"
                }
            }
            response = make_response(responseData)
            
        return response
    
    @staticmethod
    def get_all_teachers():
        users = db['users']
        
        return users.find({"role":"teacher"})
    
    @staticmethod
    def get_all_students():
        users = db['users']
        
        return users.find({"role": "student"})
    
    @staticmethod
    def get_all_departments():
        departments = db['departments']
        
        return departments.find({})
    
    @staticmethod
    def update_teacher(teacherToUpdate,_toSet):
        users = db['users']
        
        _filter = {
            "_id": teacherToUpdate
        } 
        try:
            users.update_one(_filter,{'$set': _toSet})
            return make_response({
                "status": 200
            })
        except: 
            return make_response({
                "status": 400
            })
            
    @staticmethod
    def update_student(studentToUpdate, _toSet):
        users = db['users']
        
        _filter = {
            "_id": studentToUpdate
        }
        
        try:
            users.update_one(_filter,{'$set': _toSet})
            return make_response({
                "status":200
            })
        except:
            return make_response({
                "status": 400
            })
            