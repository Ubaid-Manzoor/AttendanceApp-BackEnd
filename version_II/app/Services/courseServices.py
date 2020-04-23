from app import db
from pymongo.errors import WriteError
from flask import jsonify
import datetime  

from app.helpers.data_helper import get_student_rolls


class courseServices():
    
    @staticmethod
    def get_all_courses(filters=None,projection=None):
        # filters = None if filters
        
        courses = db['courses']
        return courses.find(filter=filters,projection=projection)
    
    @staticmethod
    def getCourse(filter=None, projection=None):
        courses = db['courses']
        return courses.find_one(filter=filter)
    
    @staticmethod
    def courseExists(courseName,department):
        courses = db['courses']
        return courses.find_one({"name":courseName,"department":department})
        
    @staticmethod
    def add_course(courseData):
        courses = db['courses']

        courseData.update({
            "student_enrolled":[]
        })
        
        responseData = {
            "status": 200,
            "result": {}
        }
        
        
        if(courses.find_one({"name":courseData['name'],"department":courseData['department']})):
            responseData["result"] = {
                        "status":409,
                        "message": "course Already Exist"
                    }
        else:    
            try:
                courses.insert_one(courseData)
                responseData["result"]={
                            "status":201,
                            "message": "Course Create"
                        }
            except WriteError as werror:
                responseData["result"]={
                            "status":400,
                            "message": werror._message
                        }

        return jsonify(responseData)
    
    
    @staticmethod
    def mark_present(student_roll,courseData):
        courses = db['courses']

        courses.find_one_and_update({**courseData,
                        },
                        {"$set": { "attendance.$[ele].attendance_on_date.$[rollno]":{"roll_no": student_roll,"status":True} }},
                        array_filters= [{"ele.date":datetime.datetime.utcnow().strftime("%Y-%m-%d")}
                                          ,{"rollno.roll_no": student_roll}],
                        upsert=False
                       )
        
    @staticmethod
    def mark_absent(student_roll,courseData):
        print("absent : ",student_roll)
        
        
    @staticmethod
    def mark_all_absent(courseData):
        courses = db['courses']
        course  = courses.find_one({**courseData
                             ,"attendance.date": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        })
        
        
        ## CHECK IF THERE IS NO STUDENT ENROLLED 
        
        if(not course):
            student_enrolled = courses.find_one({**courseData})['student_enrolled']
            print("++++++")
            student_rolls = get_student_rolls(student_enrolled)

            attendance_on_date = []
            for student_roll in student_rolls:
                student_attendance = {
                    "roll_no" : student_roll,
                    "status" : False
                }
                
                attendance_on_date.append(student_attendance)

            courses.update({**courseData},{"$push": {"attendance": {
                    "date": datetime.datetime.utcnow().strftime("%Y-%m-%d") ,
                    "attendance_on_date": attendance_on_date
                }}})
        
        
    @staticmethod
    def checkStatus(attendance_array,roll_no):
        for attendance in attendance_array:
            if attendance['roll_no'] == roll_no:
                return attendance['status']         
        return False
    @staticmethod
    def getAttendance(filters,others):
        courses = db['courses']
        month = others['month']
        all_or_one = others['all_or_one']
        roll_no = others['roll_no'] ## Will ne None if all_or_one = "all"
        
        course = courses.find_one({**filters})
        
        attendances = course['attendance']
        student_enrolled = sorted([student['roll_no'] for student in course['student_enrolled']])
        
        attendance_of_month = {}
        for attendance in attendances:
            ## First Check for the Date
            date = attendance['date']
            ## ONLY ADD THE ATTENDCE FOR REQUIRED MONTH
            
            if int(date.split('-')[1]) == int(month) + 1: ## CHECKING FOR THE MONTH
                current_day_attendance = attendance['attendance_on_date']
                
                ### If attendance of Just One Student is Requested
                if all_or_one == "one":
                    day = int(date.split('-')[2])
                    present = courseServices.checkStatus(current_day_attendance,roll_no)
                    
                    ### If we have to add Student attence for the first time
                    ### then enter IF otherwise ELSE
                    if not attendance_of_month.get(roll_no):
                        attendance_of_month[roll_no] = [{"day": day,"present": present}]
                    else:
                        attendance_of_month.get(roll_no).append({"day": day,"present": present})
                ### If attendance of Just All Students is Requested
                else:
                    for roll_no in student_enrolled:
                        if not attendance_of_month.get(roll_no):
                            attendance_of_month[roll_no] = {"totalClassesAttended": 0, "totalClasses":0}
                        else:
                            attendance_of_month[roll_no] =  {
                                                                "totalClassesAttended": attendance_of_month[roll_no]['totalClassesAttended'] \
                                                                                            + courseServices.checkStatus(current_day_attendance,roll_no)
                                                               ,"totalClasses": attendance_of_month[roll_no]['totalClasses'] + 1
                                                            }

        return attendance_of_month