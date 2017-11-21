
# User-related endpoint definitions

from flask import request, Blueprint
from models.user import User
from responses.standard_response import json_response

# Declare Blueprint

user_endpoints = Blueprint('user_endpoints', __name__)

# Create Profile

@user_endpoints.route("/create_profile", methods = ['POST'])
def create_profile():
    username = request.get_json()['username']
    password = request.get_json()['password']
    user = User.create_new_user(username, password)
    return json_response(user.login_output(), message = 'Profile created!')

# Login

@user_endpoints.route("/login", methods = ['POST'])
def login():
	username = request.get_json()['username']
	password = request.get_json()['password']
	user = User.authenticate_password(username, password)
	return json_response(user.login_output(), message = 'Successful login!')

# Profile Public View

@user_endpoints.route("/public_view_profile/<sought_user_id>", methods = ['POST'])
def public_view_profile(sought_user_id):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	User.authenticate_token(user_id, token)
	user = User.return_by_user_id(sought_user_id)
	return json_response(user.public_output())

# Profile Owner View

@user_endpoints.route("/owner_view_profile/<sought_user_id>", methods = ['POST'])
def owner_view_profile(sought_user_id):
	token = request.get_json()['token']
	user = User.authenticate_token(sought_user_id, token)
	return json_response(user.owner_output())

# Update Profile

@user_endpoints.route("/update_profile/<user_id>", methods = ['POST'])
def update_profile(user_id):
	data = request.get_json()
	user = User.authenticate_token(user_id, data['token'])
	user = user.update_profile(data)
	return json_response(user.owner_output(), message = 'Profile updated!')


