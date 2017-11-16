
# API definitions
from flask import Flask, request, Response
from models import *

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def hello():
    return "Hello World!"

@app.route("/create_profile", methods = ['POST'])
def create_profile():
	x = request.get_json()
	y = User.create_new_user(x)