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
    def get_all_students_enrolled(name:str, department:str, semester:int):
        courses = db['courses']
        return courses.find_one({"name":name,"department": department, "semester":semester})['student_enrolled']
    
    

    @staticmethod
    def get_encodings(class_name):
        pass 


    
    
            