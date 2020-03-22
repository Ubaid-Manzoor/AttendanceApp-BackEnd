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
        dataToSend = {
            "username" : student['_id'],
            "name" : student['name'],
            "department" : student['department'],
            "semester" : student['semester'],
            "confirmed": student['confirmed']
        }
        allStudents.append(dataToSend)
        
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