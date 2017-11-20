# Endpoint definitions


# Imports

from flask import Flask, request, jsonify

from models.user import User

from standard_error import StandardError
from standard_response import json_response


# Initialize Flask App

app = Flask(__name__)


# Hello World

@app.route("/")
def hello():
    return "Hello World!"

# Error Handler

@app.errorhandler(StandardError)
def handle_standard_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Create Profile

@app.route("/create_profile", methods = ['POST'])
def create_profile():
    username = request.get_json()['username']
    password = request.get_json()['password']
    user = User.create_new_user(username, password)
    return json_response(user.login_output(), message = 'Profile created!')

# Login

@app.route("/login", methods = ['POST'])
def login():
	username = request.get_json()['username']
	password = request.get_json()['password']
	user = User.authenticate_password(username, password)
	return json_response(user.login_output(), message = 'Successful login!')

# Profile Public View

@app.route("/public_view_profile/<sought_user_id>", methods = ['POST'])
def public_view_profile(sought_user_id):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	if User.authenticate_token(user_id, token):
		user = User.return_by_user_id(sought_user_id)
		return json_response(user.public_output())

# Profile Owner View

@app.route("/owner_view_profile/<sought_user_id>", methods = ['POST'])
def owner_view_profile(sought_user_id):
	token = request.get_json()['token']
	user = User.authenticate_token(sought_user_id, token)
	return json_response(user.owner_output())

# Update Profile

@app.route("/update_profile/<user_id>", methods = ['POST'])
def update_profile(user_id):
	data = request.get_json()
	user = User.authenticate_token(user_id, data['token'])
	user = user.update_profile(data)
	return json_response(user.owner_output(), message = 'Profile updated!')



