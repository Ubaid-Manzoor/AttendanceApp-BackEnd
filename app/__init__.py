from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

client = MongoClient(host='localhost',port=27017)
db = client.AttendenceSystem
print(db)
print("Database Created")


CORS(app=app, support_credentials=True)


from app.Controllers import controller
