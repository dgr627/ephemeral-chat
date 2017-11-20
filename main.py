# Endpoint definitions


# Imports

from flask import Flask, request, jsonify
from endpoints.user_endpoints import user_endpoints



# Initialize Flask App

app = Flask(__name__)
app.register_blueprint(user_endpoints)

# Hello World

@app.route("/")
def hello():
    return "Hello World!"

# Error Handler

@app.errorhandler(StandardError)
def handle_standard_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


