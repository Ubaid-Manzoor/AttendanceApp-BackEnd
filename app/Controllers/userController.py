from flask import request,jsonify,make_response
from app import app
import cv2
from PIL import Image
# from cv2 import cv
import face_recognition
# import face_recognition
import pymongo
import numpy as np
import os
import json
import random
# import jwt
from app.helpers.data_helper import extract_json, generate_student_encoding, get_student_encoding, get_student_names 
from app.helpers.image_helper import generate_image_encoding

from app.Services.courseServices import  courseServices
from app.Services.departmentServices import departmentServices
from app.Services.userServices import userServices




@app.route('/signup',methods=['POST'])
def signup():
    user_data = json.loads(request.data.decode('utf8'))

    return userServices.signup(user_data)



@app.route('/login',methods=['POST'])
def login():
    user_data = json.loads(request.data.decode('utf8'))
    
    username = user_data['username']
    password = user_data['password']

    return userServices.login(username,password)


@app.route('/get_user',methods=['POST'])
def get_user():
    
    print(json.loads(request.data.decode('utf8')))
    
    username = json.loads(request.data.decode('utf8'))['username']
    return userServices.get_user(username)



@app.route('/get_all_teachers',methods=['POST'])
def get_all_teachers():
    curser = userServices.get_all_teachers()
    
    allTeachers = []
    for teacher in curser:
        dataToSend = {
            "username": teacher['_id'],
            "name": teacher['name'],
            "department": teacher['department'],
            "confirmed" : teacher['confirmed']
        }
        allTeachers.append(dataToSend)
        
    return make_response({
        "allTeachers": allTeachers
    })
    
    
@app.route('/get_all_students',methods=['POST'])
def get_all_students():
    curser = userServices.get_all_students()
    
    allStudents = []
    for student in curser:
        student['username'] = student.pop('_id')
        # dataToSend = {
        #     "username" : student['_id'],
        #     "name" : student['name'],
        #     "department" : student['department'],
        #     "semester" : student['semester'],
        #     "confirmed": student['confirmed']
        # }
        allStudents.append(student)
        
    return make_response({
        "allStudents" : allStudents
    })
    

    
@app.route('/update_teacher',methods=['POST'])
def update_teacher():
    updateData = json.loads(request.data.decode('utf8'))
    print("updateData : ",updateData)
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return userServices.update_teacher(whomToUpdate,whatToUpdate)
    

@app.route('/update_student',methods=['POST'])
def update_sudent():
    updateData = json.loads(request.data.decode('utf8'))
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return userServices.update_student(whomToUpdate,whatToUpdate)

app.config["IMAGE_UPLOAD_PATH"] = "/home/ubaid/Desktop/MyDrive/Projects/Attendance-App/backend/app/static/images"


@app.route('/enroll_student',methods=['POST'])
def enroll_student():
    
    ##########################################
    ################ FROM DATA ###############
    courseData = json.loads(request.form.get('courseData'))
    student_roll = request.form.get('roll_no')
    # print(image)
    imagestr = request.files['file']
    
    path = os.path.join(app.config["IMAGE_UPLOAD_PATH"],student_roll)
    
    imagestr.save(path)    
    imageLoaded = cv2.imread(path)

    student_image_encoding = face_recognition.face_encodings(imageLoaded)[0]
    
    responseObjectArray = []
    for course,condition in courseData.items():
        if condition:    
            student_data = {
                "roll_no": student_roll,
                "encoding": list(student_image_encoding)
            }
            print(course)
            courseResponse = userServices.enroll_student(course,student_data)
            
            responseObjectArray.append(courseResponse)
    # print(request.form)
    
        
    return jsonify(responseObjectArray)