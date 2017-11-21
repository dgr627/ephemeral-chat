
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

