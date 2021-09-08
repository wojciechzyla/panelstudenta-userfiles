#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import wraps
import json
from flask import request, Response
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def is_authenticated(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        message = {"info": "your are not authenticated"}
        resp = Response(json.dumps(message), status=401, mimetype='application/json')
        try:
            login = os.environ.get("USER_LOGIN")
            password = os.environ.get("USER_PASSWORD")
            provided_login = request.json["USER_LOGIN"]
            provided_password = request.json["USER_PASSWORD"]
        except KeyError:
            return resp

        if login == provided_login and password == provided_password:
            return func(*args, **kwargs)
        else:
            return resp

    return decorator
