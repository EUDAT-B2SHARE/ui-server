# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask.ext.jsonpify import jsonify
from flask import Response, g, redirect, url_for, make_response
from werkzeug.routing import Rule
from functools import wraps

from model import User, Deposit
import json, sys


app = Flask(__name__)

# default headers
headers = {'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': 'http://localhost:8000',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, Access-Control-Expose-Headers',
    'Access-Control-Expose-Headers': 'X-Token',
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



class Helper(object):
    @classmethod
    def abort(cls, code, error_msg, base):
        jj = jsonify({'error': {"message": error_msg, "base": base }})
        return jj, code

    @classmethod
    def user_authentication(cls):
        # get auth header
        auth = request.headers.get('Authorization', None)
        prefix = "B2SHARE"
        token = None
        # strip prefix
        if auth and auth[0:len(prefix)] == prefix:
            token = auth[len(prefix)+1:]
        # load user that matches token
        user = User.find_user(token=token)
        # return token, user tuple
        return (token, user)

# server payload
class B2shareServer(object):
    @classmethod
    def serve(cls):
        # debug = reloading on codechange
        app.run(debug = True, host='0.0.0.0')

    # USER

    # @app.endpoint('user#index')
    # @default_headers
    # def user_index():
    #     json = jsonify(Factory.users())
    #     return json, 200

    @app.endpoint('user#authenticate')
    @default_headers
    def user_login(methods=["POST", "OPTIONS"]):
        if request.method == "OPTIONS":
            return jsonify({}), 200
        try:
            jdata = json.loads(request.data)
            user = User.find_user(email=jdata['email'], password=jdata['password'])
            if user == None:
                return Helper.abort(401, "Unauthorized", base="Invalid credentials")
            # return user.to_json(), 200
            resp = Response(user.to_json())
            resp.code = 200
            resp.headers['X-Token'] = "B2SHARE " + user.get_token()
            return resp
        except KeyError:
            return Helper.abort(400, "Bad Request", base="Invalid credentials")

    # DEPOSIT

    @app.endpoint('deposit#index')
    @default_headers
    def deposit_index(methods=["GET", "OPTIONS"]):
        if request.method == "OPTIONS":
            return jsonify({}), 200
        try:
            # authentication
            token, user = Helper.user_authentication()
            if token and user == None:
                return Helper.abort(401, "Unauthorized", base="Invalid credentials")
            # ordering
            order_by = request.args.get('order_by', 'created_at')
            order = request.args.get('order', 'desc')
            # pagination
            size = int(request.args.get('page_size', 10))
            if size > 10 and size < 1:
                size = 10
            page = int(request.args.get('page', 1))
            if page < 1:
                page = 1
            # get deposit
            ds = Deposit.get_deposits(size=size, page=page, order_by=order_by,
                order=order, user=user)
            resp = Response(Deposit.to_deposits_json(ds))
            resp.code = 200
            if user:
                resp.headers['X-Token'] = "B2SHARE " + user.get_token()
            return resp
        except:
            return Helper.abort(500, "Internal Server Error", base="Internal Server Error")

    @app.endpoint('deposit#deposit')
    @default_headers
    def deposit(methods=["GET", "OPTIONS"]):
        if request.method == "OPTIONS":
            return jsonify({}), 200
        try:
            # authentication
            token, user = Helper.user_authentication()
            if token and user == None:
                return Helper.abort(401, "Unauthorized", base="Invalid credentials")

            # request
            uuid = request.args.get('uuid', None)
            if uuid == None:
                return Helper.abort(400, "Bad Request", base="Unknown Deposit request")

            deposit = Deposit.find_deposit(uuid=uuid, user=user)
            if deposit == None:
                return Helper.abort(404, "Not Found", base="Deposit not found")
            resp = Response(deposit.to_json())
            resp.code = 200
            if user:
                resp.headers['X-Token'] = "B2SHARE " + user.get_token()
            return resp
        except:
            return Helper.abort(500, "Internal Server Error", base="Internal Server Error")

    @app.route("/")
    @default_headers
    def index():
        return Helper.abort(404, "Not Found", base="Not found")


# routes
# app.url_map.add(Rule('/users.json', endpoint="user#index"))
app.url_map.add(Rule('/user/authenticate.json', endpoint="user#authenticate"))
app.url_map.add(Rule('/deposit/index.json', endpoint="deposit#index"))
app.url_map.add(Rule('/deposit/deposit.json', endpoint="deposit#deposit"))



