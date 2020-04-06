from app import app
import json
from flask import request
from app.Services.userServices import userServices


@app.route('/signup',methods=['POST'])
def signup():
    user_data = json.loads(request.data.decode('utf8'))

    return userServices.signup(user_data)



@app.route('/login',methods=['POST'])
def login():
    user_data = json.loads(request.data.decode('utf8'))
    
    print(user_data)
    username = user_data['username']
    password = user_data['password']

    return userServices.login(username,password)


@app.route('/get_user',methods=['POST'])
def get_user():
    
    print(json.loads(request.data.decode('utf8')))
    
    username = json.loads(request.data.decode('utf8'))['username']
    return userServices.get_user(username)




    
    

    

    

    

