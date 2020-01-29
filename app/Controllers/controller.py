from flask import request,jsonify
from app import app
import face_recognition
import pymongo
import numpy as np
import json
import random
from app.helpers.data_helper import extract_json, generate_student_encoding, get_student_encoding, get_student_names 
from app.helpers.image_helper import generate_image_encoding
from app.Services.DatabaseServices import DatabaseServices as dbServices



@app.route('/')
def home():
    return "Attendence System"

@app.route('/initiate_attendence',methods=['POST','GET'])
def initiate_attendence():
    if request.method == 'POST':
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


        return f"{len(face_encodings)} Faces Found"
    return "GET REQUEST"


@app.route('/enroll_student_to_course',methods=['POST','GET'])
def enroll_student_to_course():
    if request.method == "POST":
        data = extract_json(request.data)

        student_data  = data['student_data']
        student_data['encoding'] = generate_student_encoding()

        course_name = data['course_name']

        dbServices.enroll_student(course_name,student_data)

        return jsonify(student_data)
    return "GET REQUEST"


@app.route('/add_teacher',methods=['POST','GET'])
def add_teacher():
    if request.method == "POST":
        print(request.data)
        return "Ubaid"
    return "GET REQUEST"


@app.route('/add_course',methods=['POST'])
def add_course():
    if request.method == "POST":
        course_name = json.loads(request.data.decode('utf8'))['name']
        post = dbServices.add_course(course_name)
        return jsonify(post)
    return "GET REQUEST"
