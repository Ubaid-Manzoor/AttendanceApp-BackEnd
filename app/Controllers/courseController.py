from flask import request,jsonify,make_response
from app import app
# import face_recognition
import pymongo
import numpy as np
import json
import random
# import jwt
from app.helpers.data_helper import extract_json, generate_student_encoding, get_student_encoding, get_student_names 
from app.helpers.image_helper import generate_image_encoding

from app.Services.courseServices import  courseServices
from app.Services.departmentServices import departmentServices
from app.Services.userServices import userServices


@app.route('/add_course',methods=['POST'])
def add_course():
    # Structur of "data"
    # data = {
    #     "name": "",
    #     "teacherAssigned"
    # }
    courseData = json.loads(request.data.decode('utf8'))
    # course_name = courseData['courseName']
    # teacherAssigned = courseData['teacherAssigned']
    return courseServices.add_course(courseData)


@app.route('/get_all_courses',methods=['POST'])
def get_all_courses():
    curser = courseServices.get_all_courses()
    
    allCourses = []
    for course in curser:
        del course['student_enrolled']
        del course['_id']        
        allCourses.append(course)
    
    response = make_response({
        "allCourses":allCourses
    })
    
    return response


@app.route('/enroll_student_to_course',methods=['POST'])
def enroll_student_to_course():
    # # Structure of "data"
    # data = {
    #     "course_name": "",
    #     "student_data": {
    #         "name": "",
    #         "roll_no": "",
    #         "encoding": [] // For now generated Manually
    #     }
    # }
    
    data = extract_json(request.data)
    print(data)
    student_data  = data['student_data']
    student_data['encoding'] = generate_student_encoding()

    course_name = data['course_name']
    
    return userServices.enroll_student(course_name,student_data)