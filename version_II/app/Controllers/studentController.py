from app import app
import json
import os
import cv2
import face_recognition
from flask import jsonify, request
from app.Services.studentServices import studentServices

@app.route('/get_all_students',methods=['POST'])
def get_all_students():
    data = json.loads(request.data.decode('utf8'))
    filters = data['filters']
    projection = data['projection']
    filters = None if not filters else filters 
    projection = None if  not projection else projection
    
    print("***********************")
    print(filters)
    
    try:
        filters['_id'] = filters.pop('username')
    except: pass    
    
    curser = studentServices.get_all_students(filters, projection)
    
    allStudents = []
    for student in curser:
        student['username'] = student.pop('_id')
        allStudents.append(student)
        
    return jsonify({
        "allStudents" : allStudents
    })
    
    
@app.route('/update_student',methods=['POST'])
def update_sudent():
    updateData = json.loads(request.data.decode('utf8'))
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return studentServices.update_student(whomToUpdate,whatToUpdate)



@app.route('/enroll_student',methods=['POST'])
def enroll_student():
    """Enroll The Student Passed Through Request With Its Image"""
    ################ FROM DATA ###############
    courseData = json.loads(request.form.get('courseData'))
    student_roll = request.form.get('roll_no')
    imagestr = request.files['file']
    ##########################################
    
    ### SAVING THE IMAGE 
    path = os.path.join(app.config["IMAGE_UPLOAD_PATH"],student_roll)
    imagestr.save(path) 
    
    ### READING IMAGE BACK   
    imageLoaded = cv2.imread(path)

    ### CREATING ENCODING OF THE FACE OF THE STUDENT
    student_image_encoding = face_recognition.face_encodings(imageLoaded)[0]
    
    responseObjectArray = []
    ######## LOOP THROUGH ALL THE COURSE TO ENROLL ########### 
    for course,condition in courseData.items():
        # IF CONDITION === TRUE(TRUE IF CLICKED THE CHECKBOX WHILE ENROLLING) 
        #    ONLY THEN ENROLL STUDENT TO THE COURSE
        if condition:    
            student_data = {
                "roll_no": student_roll,
                "encoding": list(student_image_encoding)
            }
            courseResponse = studentServices.enroll_student(course,student_data)
            responseObjectArray.append(courseResponse)
    return jsonify(responseObjectArray)