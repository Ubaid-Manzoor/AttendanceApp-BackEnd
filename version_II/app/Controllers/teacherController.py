from app import app

import json 
from flask import jsonify,request
from app.Services.teacherServices import teacherServices


@app.route('/get_all_teachers',methods=['POST'])
def get_all_teachers():
    curser = teacherServices.get_all_teachers()
    
    allTeachers = []
    for teacher in curser:
        dataToSend = {
            "username": teacher['_id'],
            "name": teacher['name'],
            "department": teacher['department'],
            "confirmed" : teacher['confirmed']
        }
        allTeachers.append(dataToSend)
        
    return jsonify({
        "allTeachers": allTeachers
    })

@app.route('/update_teacher',methods=['POST'])
def update_teacher():
    updateData = json.loads(request.data.decode('utf8'))
    print("updateData : ",updateData)
    whatToUpdate = updateData['whatToUpdate']
    whomToUpdate = updateData['whomToUpdate']
    
    return teacherServices.update_teacher(whomToUpdate,whatToUpdate)