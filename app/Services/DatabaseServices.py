#CRUD Related Services
from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from pymongo.errors import WriteError
from flask import jsonify
import jwt

class DatabaseServices():

    @staticmethod
    def initiate_database():
        ##Create Courses Collection
        Courses.create()

        ##Create Users Collection
        Users.create()

    @staticmethod
    def get_all_students_enrolled(course_name:str):
        courses = db['courses']
        return courses.find_one({"_id":course_name})

    @staticmethod
    def get_encodings(class_name):
        pass 


    @staticmethod
    def add_course(course_name:str):
        courses = db['courses']
        post = {"_id":course_name,"student_enrolled":[]}
        
        ## Initializing Message and status for response 
        message = f"{course_name} course got created!!!"
        status = 201
        try:
            courses.insert_one(post)
        except WriteError as werror:
            message = werror._message
            status = 400
        return jsonify({
                "status": status,
                "message": message
        })

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
    def mark_present(student_roll):
        pass 

    @staticmethod
    def mark_absent(student_roll):
        pass


    @staticmethod
    def get_user(username, password):
        user = {
            "username": "username",
            "role":"admin"
        }
        if(user):
            return user
        else:
            return {}
        

    @staticmethod
    def signup(user):
        users = db['users']
        post = {
            "_id": user['username'],
            "password": user['password'],
            "role": user['role']
        }

        message = ""
        status = 200

        try:
            users.insert_one(post)
            message="User got successfully added!!"
        except WriteError as werror:
            message = werror
            status = 400

        return jsonify({
            "message": message,
            "status": status
        })


    @staticmethod
    def get_user(username,password):
        Users = db['users']
        
        return Users.find_one({"_id": username,"password":password})


    @staticmethod
    def login(username,password):
        user = DatabaseServices.get_user(username,password)
        
        if(user):
            jwToken = jwt.encode(user,username).decode()
            
            response = jsonify({
                "status":200,
                "result":{
                    "jwt":jwToken,
                    "status": 200,
                    "message": "user does exist"
                }
            })
        else:
            response = jsonify({
                "status": 200,
                "result":{
                    "status": 201,
                    "message": "username or password is wrong"
                }
            })

        return response