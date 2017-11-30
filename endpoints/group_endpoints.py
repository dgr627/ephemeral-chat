
# Group endpoints definitions

from flask import request, Blueprint
from responses.standard_response import json_response
from models.group import Group
from models.user import User

# Declare Blueprint

group_endpoints = Blueprint('group_endpoints', __name__)

# Create Group

@group_endpoints.route("/group/create", methods = ['POST'])
def create_group():
	data = request.get_json()
	user = User.authenticate_token(data['user_id'], data['token'])
	group = Group.create_new_group(data)
	return json_response(group.info_output(), message = 'Group created!')

@group_endpoints.route("/group/info/<group_id>", methods = ['POST'])
def view_group_info(group_id):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	user = User.authenticate_token(user_id, token)
	user.check_ismember(group_id)
	group = Group.return_by_group_id(group_id)
	return json_response(group.info_output())

@group_endpoints.route("/group/update/<group_id>", methods = ['POST'])
def update_group_info(group_id):
	data = request.get_json()
	user = User.authenticate_token(data['user_id'], data['token'])
	user.check_ismember(group_id)
	group = Group.return_by_group_id(group_id)
	group = group.update_group_info(data)
	return json_response(group.info_output(), message = "Group updated!")

@group_endpoints.route("/group/messages/<group_id>", methods = ['POST'])
def view_group_message_ids(group_id):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	user = User.authenticate_token(user_id, token)
	user.check_ismember(group_id)
	group = Group.return_by_group_id(group_id)
	return json_response(group.message_list_output())