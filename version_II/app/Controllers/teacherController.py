from app import app

import json 
from flask import jsonify,request
from app.Services.teacherServices import teacherServices


@app.route('/get_all_teachers',methods=['POST'])
def get_all_teachers():
    
    filters = json.loads(request.data.decode('utf8'))['filters']
    projection = json.loads(request.data.decode('utf8'))['projection']
    filters = None if not filters else filters 
    projection = None if  not projection else projection
    
    print("*********************")
    print("*********************")
    print("*********************")
    print("*********************")
    print(filters)
    print(projection)
    
    try:
        filters['_id'] = filters.pop('username')
    except:
        pass
    
    curser = teacherServices.get_all_teachers(filters, projection)
    
    allTeachers = []
    for teacher in curser:
        try:
            teacher['username'] = teacher.pop('_id')
        except: pass
        allTeachers.append(teacher)
    
    print("*********************")
    print("*********************")
    print("*********************")
    print("*********************")
    print(allTeachers)
    print("*********************")
    print("*********************")
    print("*********************")
        
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