
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

@message_endpoints.route("/post_message/<groupname>", methods = ['POST'])
def create_message(groupname):
	data = request.get_json()
	User.authenticate_token(data['user_id'], data['token'])
	message = Message.create_message(groupname = groupname, data = data)
	return json_response(message.message_output(), message = "Message posted!")

@message_endpoints.route("/view_message/<msg_id>", methods = ['POST'])
def view_message(msg_id):
	data = request.get_json()
	User.authenticate_token(data['user_id'], data['token'])
	return json_response(Message.return_by_msg_id(msg_id))