#CRUD Related Services
from app import db
from app.Collections.Courses import Courses 
from pymongo.errors import WriteError
from flask import jsonify

class DatabaseServices():

    @staticmethod
    def initiate_database():
        ##Create Courses Collection
        Courses.create()

        ##Create Attendance Collection
        

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

