from flask import request,jsonify
from app import app
import json

from app.Services.departmentServices import departmentServices


@app.route('/get_all_departments',methods=['POST'])
def get_all_departments():
    curser = departmentServices.get_all_departments()
    
    allDepartments = []
    for department in curser:
        dataToSend = {
            "name" : department['name']
        }
        
        allDepartments.append(dataToSend)
        
    return jsonify({
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