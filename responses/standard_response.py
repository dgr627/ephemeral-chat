# Standard Response Class
# Contains data, HTTP status code, custom message string

from flask import jsonify, make_response

def json_response(response, message = None, status = 200, headers = None):
	rv = {"success" : True, "message": message, "data" : response}
	return make_response(jsonify(rv), status, headers)
