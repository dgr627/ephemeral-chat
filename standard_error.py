from flask import jsonify

class StandardError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, data=None):
        Exception.__init__(self)
        self.message = message
        self.success = False
        if status_code is not None:
            self.status_code = status_code
        self.data = data

    def to_dict(self):
        rv = dict(self.data or ())
        rv['message'] = self.message
        return rv