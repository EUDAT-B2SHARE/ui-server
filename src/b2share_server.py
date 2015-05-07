from flask import Flask
from flask import request
from flask.ext.jsonpify import jsonify
from flask import Response, g, redirect, url_for, make_response
from werkzeug.routing import Rule
from functools import wraps

import sha



app = Flask(__name__)

# default headers
headers = {'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': 'http://localhost:8000',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Server': 'EUDAT-B2SHARE/UI-API-1.1.1'}

# helpers for response headers
def add_response_headers(headers={}):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def default_headers(f):
    @wraps(f)
    @add_response_headers(headers)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

# routes
app.url_map.add(Rule('/users.json', endpoint="user#index"))
app.url_map.add(Rule('/user/login.json', endpoint="user#login"))


class Helper(object):
    @classmethod
    def to_hash(cls, email, password):
        return sha.new(email + ":" + password).hexdigest()

    @classmethod
    def make_user(cls, name, email, password):
        return jsonify({'user': {
                'email': email, 'name': name,
                'password': Helper.to_hash(email, password)
            }})

    @classmethod
    def login(cls, email, password):
        return False

    @classmethod
    def abort(cls, code, error_msg):
        json = jsonify({'error': code, "message": error_msg})
        return json, code

class Factory(object):

    @classmethod
    def user_dennis(cls):
        return Helper.make_user(name="Dennis Blommesteijn",
            email="dennis.blommesteijn@surfsara.nl", password="dennis123")

    @classmethod
    def user_walter(cls):
        return Helper.make_user(name="Walter de Jong",
            email="walter.dejong@surfsara.nl", password="walter123")

    @classmethod
    def users(cls):
        users = {'users': [ Factory.user_dennis(), Factory.user_walter() ]}


class B2shareServer(object):
    @classmethod
    def serve(cls):
        # debug = reloading on codechange
        app.run(debug = True)

    @app.endpoint('user#index')
    def user_index():
        json = jsonify(Factory.users())
        return json, 200

    @app.endpoint('user#login')
    @default_headers
    def user_login(methods=["POST", "OPTIONS"]):
        email = request.args.get('email', "")
        password = request.args.get('password', "")
        if (email == "" or password == "") or Helper.login(email, password):
            return Helper.abort(403, "access denied")
        json = jsonify("login")
        return json, 200




