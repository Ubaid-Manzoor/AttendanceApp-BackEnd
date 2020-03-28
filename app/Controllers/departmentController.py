from flask import request,jsonify,make_response
from app import app
# import face_recognition
import pymongo
import numpy as np
import json
import random
# import jwt
from app.helpers.data_helper import extract_json, \
                                    generate_student_encoding, \
                                    get_student_encoding
                                    
from app.helpers.image_helper import generate_image_encoding

from app.Services.courseServices import  courseServices
from app.Services.departmentServices import departmentServices
from app.Services.userServices import userServices


@app.route('/get_all_departments',methods=['POST'])
def get_all_departments():
    curser = departmentServices.get_all_departments()
    
    allDepartments = []
    for department in curser:
        dataToSend = {
            "name" : department['name']
        }
        
        allDepartments.append(dataToSend)
        
    return make_response({
        "allDepartments": allDepartments
    })
    
    
    
@app.route('/add_department', methods=['POST'])
def add_department():
    # Structure of Department
    # data = [{
    #   "name" : ""   
    #}]
    departmentData = json.loads(request.data.decode('utf8'))
    departmentName = departmentData['departmentName']
    
    return departmentServices.add_department(departmentName)