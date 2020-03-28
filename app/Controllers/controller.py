from flask import request,jsonify,make_response
from app import app
import face_recognition
import pymongo
import numpy as np
import json
import random
import jwt
import cv2
import os

from app.helpers.data_helper import extract_json, \
                                    generate_student_encoding, \
                                    get_student_encoding, \
                                    get_student_rolls 
from app.helpers.image_helper import generate_image_encoding
from app.Services.DatabaseServices import DatabaseServices as dbServices

from app.Services.courseServices import courseServices



@app.route('/')
def home():
    return "Attendence System"

@app.route('/initiate_attendence',methods=['POST'])
def initiate_attendence():
    
    courseData = json.loads(request.form.get('courseData'))
    print("+++++++++++++++++")
    print("+++++++++++++++++")
    print("+++++++++++++++++")
    print(courseData)
    print("+++++++++++++++++")
    print("+++++++++++++++++")
    
    # print(image)
    imagestr = request.files['file']
    print(imagestr)
    print(courseData)
    try: 
        
        path = os.path.join(app.config["IMAGE_UPLOAD_PATH"],courseData.get('name'))
        
        imagestr.save(path)    
        imageLoaded = cv2.imread(path)

        class_image_encodings = face_recognition.face_encodings(imageLoaded)
        
        all_student_data = dbServices.get_all_students_enrolled(**courseData)

        known_face_encodings = get_student_encoding(all_student_data)
        all_student_roll_nos = get_student_rolls(all_student_data)

        courseServices.mark_all_absent(courseData)

        for face_encoding,student_roll in zip(class_image_encodings,all_student_roll_nos):
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                courseServices.mark_present(student_roll,courseData)
        return {
            "status": 200,
            "result": {
                "status": 201,
                "message": "Attendance Done"
            }
        }
    except:
        return {
            "status": 200,
            "result": {
                "status": 400,
                "message": "Some problem check your image"
            }
        }





    


# @app.route('/add_teacher',methods=['POST'])
# def add_teacher():
#     print(request.data)
#     return "Ubaid"





    


