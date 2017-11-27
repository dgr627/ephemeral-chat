
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
	User.authenticate_token(data['user_id'], data['token'])
	group = Group.create_new_group(data)
	return json_response(group.info_output(), message = 'Group created!')

@group_endpoints.route("/group/info/<groupname>", methods = ['POST'])
def view_group_info(groupname):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	User.authenticate_token(user_id, token)
	group = Group.return_by_groupname(groupname)
	return json_response(group.info_output())

@group_endpoints.route("/group/update/<groupname>", methods = ['POST'])
def update_group_info(groupname):
	data = request.get_json()
	User.authenticate_token(data['user_id'], data['token'])
	group = Group.return_by_groupname(groupname)
	group = group.update_group_info(data)
	return json_response(group.info_output())

@group_endpoints.route("/group/messages/<groupname>", methods = ['POST'])
def view_group_message_ids(groupname):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	User.authenticate_token(user_id, token)
	group = Group.return_by_groupname(groupname)
	return json_response(group.message_list_output())