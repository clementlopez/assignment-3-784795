#coding: utf-8

from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import json
import hashlib, binascii, os
from mysimbdpstreamingestmanager import run_manager
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return render_template('index.html')

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

class Customer_Profile(Resource):
    def get(self):
        customer_id = request.args.get('id')
        password = request.args.get('password')
        with open('./users.json') as json_users:
            authent = json.load(json_users)
        if verify_password(authent[customer_id], password):
            result = {}
            print(password)
            with open(str(customer_id)+'/config.json') as json_data:
                result = json.load(json_data)
            return jsonify(result)
        return "Wrong id and/or password"

class Stream_start(Resource):
    def get(self):
        customer_id = request.args.get('id')
        password = request.args.get('password')
        with open('./users.json') as json_users:
            authent = json.load(json_users)
        if verify_password(authent[customer_id], password):
            run_manager(customer_id, "start")
            return "Stream start"
        return "Wrong id and/or password"

api.add_resource(Customer_Profile, '/customer') # Route_1
api.add_resource(Stream_start, '/start') # Route_1

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')