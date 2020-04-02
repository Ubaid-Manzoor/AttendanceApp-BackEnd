from app import db
from app.Collections.Courses import Courses 
from app.Collections.Users import Users
from app.Collections.Departments import Departments
from pymongo.errors import WriteError
from flask import jsonify, Response
import datetime 
import jwt


class teacherServices():
    @staticmethod
    def get_all_teachers(filters, projection):
        users = db['users']
        if filters is None:
            return users.find({"role": "teacher"})
        else:
            filters.update({
                "role": "teacher"
            })
            return users.find(filter=filters, projection=projection)
    
    @staticmethod
    def update_teacher(teacherToUpdate,_toSet):
        users = db['users']
        
        _filter = {
            "_id": teacherToUpdate
        } 
        try:
            users.update_one(_filter,{'$set': _toSet})
            return jsonify({
                "status": 200
            })
        except: 
            return jsonify({
                "status": 400
            })