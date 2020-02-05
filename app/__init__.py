from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app=app, support_credentials=True)


client = MongoClient(host='localhost',port=27017)
db = client.AttendenceSystem


## Initialize Database
from app.Services.DatabaseServices import DatabaseServices as dbServices
print("Here")
dbServices.initiate_database()







from app.Controllers import controller


