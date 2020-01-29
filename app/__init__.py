from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)

client = MongoClient(host='localhost',port=27017)
db = client.AttendenceSystem


##Create Collections in Database

##1) Create Courses Collection
from app.Services.DatabaseServices import DatabaseServices as dbServices

dbServices.initiate_database()

##2) Create Attendance Collection




CORS(app=app, support_credentials=True)


from app.Controllers import controller


