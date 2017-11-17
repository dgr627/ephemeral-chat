# API definitions
from flask import Flask, request, jsonify
from models import *
from standard_error import StandardError

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


@app.route("/create_profile", methods=['POST'])
def create_profile():
    result = User.create_new_user(request.get_json())
    print result
    try:
        return jsonify(result)
    except Exception as e:
        print(e)


@app.errorhandler(StandardError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    response.success = False
    return response