from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, make_response, Response
import datetime 
import jwt


class userServices():
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
    def signup(userData:dict):
        users = db['users']
        
        userData['_id'] = userData.pop('username')
        userData.update({
            "confirmed": userData['confirmed'] if userData['confirmed'] else False

        })
        # userData = {
        #     "_id": user['username'],
        #     "name": user['name'],
        #     "department": user['department'],
        #     "password": user['password'],
        #     "role": user['role'],
        #     "confirmed": user['confirmed'] if user['confirmed'] else False
        # }
        if(userData['role'] == "student"):
            userData['semester'] = userData['semester']


        if(userServices.usernameExists(userData['_id'])):
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
        user = userServices.check_user(username,password)
        
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
            
            