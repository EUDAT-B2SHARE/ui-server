from flask import Flask
from flask import request
from flask.ext.jsonpify import jsonify
from flask import Response, g, redirect, url_for, make_response
from werkzeug.routing import Rule
from functools import wraps

from model import User, Deposit
import json


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


class Helper(object):
    @classmethod
    def abort(cls, code, error_msg, base, ):
        jj = jsonify({'error': {"message": error_msg, "base": base }})
        return jj, code

# server payload
class B2shareServer(object):
    @classmethod
    def serve(cls):
        # debug = reloading on codechange
        app.run(debug = True)

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
            user.new_token()
            return user.to_json(), 200
        except KeyError:
            return Helper.abort(400, "Bad Request", base="Invalid credentials")

    # DEPOSIT

    @app.endpoint('deposit#index')
    @default_headers
    def deposit_index(methods=["GET", "OPTIONS"]):
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
            order=order)
        return Deposit.to_deposits_json(ds), 200


# routes
# app.url_map.add(Rule('/users.json', endpoint="user#index"))
app.url_map.add(Rule('/user/authenticate.json', endpoint="user#authenticate"))

app.url_map.add(Rule('/deposit/index.json', endpoint="deposit#index"))



