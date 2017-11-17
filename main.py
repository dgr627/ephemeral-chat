# API definitions
from flask import Flask, request, jsonify
from models.user import User
from standard_error import StandardError

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


@app.route("/create_profile", methods=['POST'])
def create_profile():
    username = request.get_json()['username']
    password = request.get_json()['password']
    result = User.create_new_user(username, password)
    try:
        return jsonify(result.to_auth_output())
    except Exception as e:
        print(e)


@app.errorhandler(StandardError)
def handle_standard_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
