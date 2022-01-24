from flask.globals import request
from flask_cors import cross_origin
from flask_login.utils import logout_user
from sympy import re
from todolist import app, db
from flask import jsonify, render_template, redirect, url_for, session, flash, request
from todolist.models import Task, User
from todolist.forms import LoginForm, RegisterForm, TaskForm
from todolist.helpers import login_required, validate_email_address, validate_username
from flask_login import login_user, current_user
import psycopg2
from todolist.storage import get_profile_pic, upload_blob, file_in_storage
import os

# structure api blueprint
from flask import Blueprint

api = Blueprint('api', __name__)

# @app.route('/')
# @app.route('/index')
# def home():
#     if current_user.is_authenticated:
#         return redirect(url_for('tasks'))
#     else:
#         return redirect(url_for('login'))


@api.route('/tasks', methods=['GET','POST', 'DELETE', 'PUT'])
# @login_required
@cross_origin
def tasks():
    response_object = {'status': 'success'}
    request_object = request.get_json()
    if request.method == "DELETE":

        # if 'done' button pressed, delete task from db
        
        done_task = Task.query.filter_by(id=request_object.get('id')).first()
        db.session.delete(done_task)
        db.session.commit()

        response_object['message'] = 'Task finished!'
        return jsonify(response_object)



    elif request.method == "POST":
        # ensure at least title entered
        if request_object.get('title') != '':
            # add task to db
            task = Task(title=request_object.get('title'),
                        description=request_object.get('description'),
                        importance=request_object.get('importance'),
                        user=session['user_id'])
        
            db.session.add(task)
            db.session.commit()

            response_object['message'] = 'Task added.'
            return jsonify(response_object)
        else:
            response_object['message'] = 'Task must have a title.'
            response_object['status'] = 400
            return jsonify(response_object)


            
    elif request.method == "PUT":
        task = Task.query.filter_by(id=request_object.get("id")).first()
        task.title = request_object.get('title')
        task.description = request_object.get('description')
        task.importance = request_object.get('importance')
        db.session.commit()

        response_object['message'] = 'Task saved.'
        return jsonify(response_object)

    # retrieve tasks from db
    tasks_object = Task.query.filter_by(user=User.query.filter_by(id=session['user_id']).first().id).all()
    tasks_list = [t.serialize for t in tasks_object]
    print(tasks_list)
    response_object['tasks'] = tasks_list
    return jsonify(response_object)

@api.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        response_object = {'status': 200}
        post_data = request.get_json()

        username = post_data.get('username')
        password = post_data.get('password')
        email = post_data.get('email')
        confirm = post_data.get('confirm')

        print(username)
        print(validate_username(username))

        if not validate_username(username):
            response_object['status'] = 400
            response_object['message'] = "Username already exists."
            return jsonify(response_object)
        
        if not validate_email_address(email):
            response_object['status'] = 400
            response_object['message'] = "Email already registered. Please login."
            return jsonify(response_object)

        if password == confirm:
            user = User(username=username,
            email=email,
            password=password)

            db.session.add(user)
            db.session.commit()

            response_object['message'] = "Account created."

            return jsonify(response_object)
        
        # error handling
        else:
            response_object['status'] = 400
            response_object['message'] = 'There was an error creating user ' + username + "."
            return jsonify(response_object)

@api.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        response_object = {'status': 200}
        post_data = request.get_json()

        username = post_data["username"]
        password = post_data["password"]

        user_id = User.query.filter_by(username=username).first()
        print(user_id)
        if not user_id:
            response_object['status'] = 400
            response_object['message'] = 'Username not found.'
            return jsonify(response_object) 

        if user_id and user_id.check_password(pass_to_check=password):
            session['user_id'] = user_id.id
            login_user(user_id)
            response_object['message'] = "Logged in as " + username + "."
            return jsonify(response_object)
        
        # error handling
        else:
            response_object['status'] = 400
            response_object['message'] = 'Username and/or Password incorrect.'
            return jsonify(response_object)

@api.route('/logout')
def logout():
    response_object = {'status': 200}
    session.clear()
    logout_user()
    return jsonify(response_object)


# @app.route('/upload', methods = ['POST'])
# @login_required
# def upload():
    
#     bucket_name = "todolist-bucket"
#     profile_pic = request.files["profile_pic"]
#     dest_filename = f"{current_user.username}-profile-pic"
#     upload_blob(bucket_name, profile_pic, dest_filename)

#     return redirect(url_for('profile'))

# @app.route('/profile')
# @login_required
# def profile():
#     # get profile pic
#     bucket = "todolist-bucket"
#     filename = f"{current_user.username}-profile-pic"
#     public_url = get_profile_pic(bucket, filename)
#     print(public_url)
#     if file_in_storage(bucket, filename):
#         profile_pic = public_url
#     else:
#         profile_pic = 'https://storage.googleapis.com/todolist-bucket/default-profile-pic'
#     return render_template('profile.html', profile_pic=profile_pic)
    