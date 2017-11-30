
# Message endpoints definitions

from flask import request, Blueprint
from models.message import Message
from models.user import User
from responses.standard_response import json_response

# Declare Blueprint

message_endpoints = Blueprint('message_endpoints', __name__)

@message_endpoints.route("/message_test")
def hello():
    return "Works!"

@message_endpoints.route("/message/post/<group_id>", methods = ['POST'])
def create_message(group_id):
	data = request.get_json()
	user = User.authenticate_token(data['user_id'], data['token'])
	user.check_ismember(group_id)
	message = Message.create_message(group_id = group_id, data = data)
	return json_response(message.message_output(), message = "Message posted!")

@message_endpoints.route("/message/view/<msg_id>", methods = ['POST'])
def view_message(msg_id):
	data = request.get_json()
	user = User.authenticate_token(data['user_id'], data['token'])
	message = Message.return_by_msg_id(msg_id)
	return json_response(message.message_output())

@message_endpoints.route("/message/delete/<msg_id>", methods = ['POST'])
def delete_message(msg_id):
	try:
		data = request.get_json()
		user = User.authenticate_token(data['user_id'], data['token'])
		message = Message.return_by_msg_id(msg_id)
		return json_response(message.delete_message(), message = "Message deleted")
	except Exception as e: print(e)