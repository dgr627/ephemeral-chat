
# Group endpoints definitions

from flask import request, Blueprint
from responses.standard_response import json_response
from models.group import Group
from models.user import User

# Declare Blueprint

group_endpoints = Blueprint('group_endpoints', __name__)

# Create Group

@group_endpoints.route("/create_group", methods = ['POST'])
def create_group():
	data = request.get_json()
	User.authenticate_token(data['user_id'], data['token'])
	group = Group.create_new_group(data)
	return json_response(group.info_output(), message = 'Group created!')

@group_endpoints.route("/group_info/<groupname>", methods = ['POST'])
def view_group_info(groupname):
	user_id = request.get_json()['user_id']
	token = request.get_json()['token']
	User.authenticate_token(user_id, token)
	group = Group.query(Group.groupname == groupname).get()
	return json_response(group.info_output())