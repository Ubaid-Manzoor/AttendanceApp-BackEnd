#CRUD Related Services
from app import db
from app.Collections.Courses import Courses 

class DatabaseServices():

    @staticmethod
    def initiate_database():
        ##Create Courses Collection
        Courses.create()

        ##Create Attendance Collection
        

    @staticmethod
    def get_all_students_enrolled(course_name:str):
        courses = db['courses']
        return courses.find_one({"_id":course_name})

    @staticmethod
    def get_encodings(class_name):
        pass 


    @staticmethod
    def add_course(course_name:str):
        courses = db['courses']
        post = {"_id":course_name,"student_enrolled":[]}
        courses.insert_one(post)

        return post

    @staticmethod
    def enroll_student(course_to_enroll,student_data):
        courses = db['courses']
        result = courses.update({"_id":course_to_enroll},{"$push":{"student_enrolled":student_data}})
        print(result)


    @staticmethod
    def mark_present(student_roll):
        pass 

    @staticmethod
    def mark_absent(student_roll):
        result: int

