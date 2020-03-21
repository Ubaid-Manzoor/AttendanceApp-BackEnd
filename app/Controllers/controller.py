from flask import request,jsonify,make_response
from app import app
import face_recognition
import pymongo
import numpy as np
import json
import random
import jwt

from app.helpers.data_helper import extract_json, generate_student_encoding, get_student_encoding, get_student_names 
from app.helpers.image_helper import generate_image_encoding
from app.Services.DatabaseServices import DatabaseServices as dbServices



@app.route('/')
def home():
    return "Attendence System"

@app.route('/initiate_attendence',methods=['POST'])
def initiate_attendence():
    json_data = json.loads(request.data.decode('utf8'))
    course_name = json_data['course_name']

    image_encodings = generate_image_encoding()#Will pass an Image in Future

    ## Get Data of All Student in The course
    all_student_data = dbServices.get_all_students_enrolled(course_name)['student_enrolled']

    known_face_encodings = get_student_encoding(all_student_data)
    all_student_roll_nos = get_student_names(all_student_data)

    print(np.array(known_face_encodings).shape)
    print(all_student_roll_nos)

    for face_encoding in image_encodings:
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)

        face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)

        best_match_index = np.argmin(face_distance)

        if matches[best_match_index]:
            print(all_student_roll_nos[best_match_index])
            print("mark_present")
            # mark_present(all_student_roll_nos[best_match_index])
        else:
            # mark_absent(all_student_roll_nos[best_match_index])
            print("mark_absent")
    return "Done"


    # return f"{len(face_encodings)} Faces Found"


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
    
    return dbServices.enroll_student(course_name,student_data)

    


@app.route('/add_teacher',methods=['POST'])
def add_teacher():
    print(request.data)
    return "Ubaid"


@app.route('/add_course',methods=['POST'])
def add_course():
    # Structur of "data"
    # data = {
    #     "name": "",
    #     "teacherAssigned"
    # }
    courseData = json.loads(request.data.decode('utf8'))
    course_name = courseData['courseName']
    teacherAssigned = courseData['teacherAssigned']
    return dbServices.add_course(course_name,teacherAssigned)
    


@app.route('/signup',methods=['POST'])
def signup():
    user_data = json.loads(request.data.decode('utf8'))

    return dbServices.signup(user_data)



@app.route('/login',methods=['POST'])
def login():
    user_data = json.loads(request.data.decode('utf8'))
    
    username = user_data['username']
    password = user_data['password']

    return dbServices.login(username,password)


@app.route('/get_user',methods=['POST'])
def get_user():
    
    username = json.loads(request.data.decode('utf8'))['username']
    return dbServices.get_user(username)

@app.route('/get_all_courses',methods=['POST'])
def get_all_courses():
    curser = dbServices.get_all_courses()
    
    allCourses = []
    for course in curser:
        dataToSend = {
            "name":course['_id'],
            "teacherAssigned":   course['teacherAssigned']
        }
        allCourses.append(dataToSend)
    
    response = make_response({
        "allCourses":allCourses
    })
    
    return response

@app.route('/get_all_teachers',methods=['POST'])
def get_all_teachers():
    curser = dbServices.get_all_teachers()
    
    allTeachers = []
    for teacher in curser:
        dataToSend = {
            "name": teacher['_id'],
            "confirmed" : teacher['confirmed']
        }
        allTeachers.append(dataToSend)
        
    return make_response({
        "allTeachers": allTeachers
    })
    
    
@app.route('/get_all_students',methods=['POST'])
def get_all_students():
    curser = dbServices.get_all_students()
    
    allStudents = []
    for student in curser:
        dataToSend = {
            "name" : student['_id'],
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
    
    return dbServices.update_teacher(whomToUpdate,whatToUpdate)
    

@app.route('/update_student',methods=['POST'])
def update_sudent():
    updateData = json.loads(request.data.decode('utf8'))
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return dbServices.update_student(whomToUpdate,whatToUpdate)
    