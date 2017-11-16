
# API definitions
from flask import Flask, request, jsonify
from models import *

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def hello():
    return "Hello World!"

@app.route("/create_profile", methods = ['POST'])
def create_profile():
	result = User.create_new_user(request.get_json())
	print result
	try:
		return jsonify(result)
	except Exception as e: print(e)
