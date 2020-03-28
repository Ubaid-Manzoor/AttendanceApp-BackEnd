import json
import random
import numpy as np

def extract_json(byte_data):
    return json.loads(byte_data.decode('utf8'))


def ConnectDatabase():
    pass

def closeDatabase():
    pass

def get_student_encoding(students_data:dict):

    # print(students_data)

    return [student_data['encoding'] for student_data in students_data]

def get_student_rolls(students_data:dict):
    return [student_data['roll_no'] for student_data in students_data]

def generate_student_encoding():
    return [random.uniform(1e-4,1e-1) for _ in range(128)]

## Attendence Schema

# {
#     "Class_name_1":{
#         "Date_1":{
#             "roll_no":True,
#             "roll_no":True,
#             "roll_no":False,
#         },
#         "Date_2":{
#             "roll_no":True,
#             "roll_no":True,
#             "roll_no":False,
#         }
#     },
#     "Class_name_2":{
#         "Date_1":{
#             "roll_no":True,
#             "roll_no":True,
#             "roll_no":False,
#         },
#         "Date_2":{
#             "roll_no":True,
#             "roll_no":True,
#             "roll_no":False,
#         }
#     }
# }

# # Class Schema

# {
#     "Class_name_1":{
#         "roll_no":{
#             "name":"",
#             "encoding":""
#         },
#         "roll_no":{
#             "name":"",
#             "encoding":""
#         }
#     },
#     "Class_name_2":{
#         "roll_no":{
#             "name":"",
#             "encoding":""
#         },
#         "roll_no":{
#             "name":"",
#             "encoding":""
#         }
#     }
# }