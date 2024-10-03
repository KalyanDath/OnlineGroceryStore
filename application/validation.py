from werkzeug.exceptions import HTTPException
from flask import make_response
from flask import current_app as app
import json


class CategoryNotFoundError(HTTPException):
    def __init__(self):
        self.response = make_response('',404)

class ValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = { "error_code" : error_code, "error_message" : error_message}
        self.response = make_response(json.dumps(data),status_code)

class CategoryExistsError(HTTPException):
    def __init__(self):
        self.response = make_response('Category Already Exists',409)

class ProductNotFoundError(HTTPException):
    def __init__(self):
        self.response = make_response('Product Not Found',404)
class ProductExistsError(HTTPException):
    def __init__(self):
        self.response = make_response('Product Already Exists',409)