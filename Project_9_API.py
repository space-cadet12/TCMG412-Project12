#Imports Required Modules for the App
from flask import Flask, jsonify, request
import hashlib
import slack
import math
import os
import requests
import redis
from redis import RedisError
app = Flask(__name__)

#Welcome Message
@app.route("/")
def welcome():
    return "<h1>Welcome to our application! Possible extensions are   /md5/string   /factorial/int /fibonacci/int   /is-prime/int  /slack-alert/string</h1>"

#String Extension
@app.route("/md5/<string>")
def md5(string):
	hash_object = hashlib.md5(string.encode())
	md5_hash = hash_object.hexdigest()
	return jsonify(input=string, output=md5_hash)

#Factorial Extension
@app.route("/factorial/<num>")
def fact(num):
	intnum = int(num)
	factorial = 1
	if intnum == 0:
		return jsonify(input=int(num), output=int(1))
	if intnum < 0:
		return jsonify('Error, please enter a positive integer')
	else:
		for i in range(1,intnum + 1):
			factorial = factorial*i
		return jsonify(input=int(num), output=int(factorial))
    

#Fibonacci Extension
@app.route('/fibonacci/<int(signed=True):x>')
def fibo(x):
    return jsonify(
        input = x,
        output = fib(x)
        )
def fib(n):
    if n < 0 :
        print ("Error, input needs to be positive.")   
    else:
        a, b = 0, 1
        array = [0]
        while b <= n:
            array.append(b)
            a, b = b, a+b   
    return array

#Prime Extension
@app.route('/is-prime/<int:x>')
def prime(x):
    return jsonify(
        input=x,
        output=is_prime(x)
        )
def is_prime(n):
    if n <= 0:
        return 'Invalid number, please input an integer higher than 0'
    if n > 2:
       for i in range(2, n):
           if (n % i == 0):
               return False      
           else:
              return True
    else:
       return True

#for slack message
@app.route('/slack-alert/<string:msg>')
def post_to_slack(msg):
	SLACK_URL = 'https://hooks.slack.com/services/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'
	# build the dictionary that will be used as the json payload
	data = { 'text': msg }
	# make an HTTP request using POST to the Slack URL
	resp = requests.post(SLACK_URL, json=data)
	# the status code that is returned from Slack tells us what happened
	if resp.status_code == 200:
        	result = True
        	mesg = "Message successfully posted to Slack channel"
	else:
        	result = False
        	mesg = "There was a problem posting to the Slack channel (HTTP response: " + str(resp.status_code) + ")."
	return jsonify(
        	input=msg,
        	output=result,
        	message=mesg
        ), 200 if resp.status_code==200 else 400

# Create a variable that represents the Redis Server
r = redis.Redis(host='redis-server', port=6379, charset="utf-8", decode_responses=True)

# Route for the new key value pair we're implementing
@app.route('/keyval', methods=['POST', 'PUT'])
def kv_upsert(): # Create a function for performing the PUT and POST
    # Create a json package to store data
    _JSON = {
        'key': None,
        'value': None,
        'command': 'CREATE' if request.method=='POST' else 'UPDATE',
        'result': False,
        'error': None
    }

    # Make sure json data input is valid
    try:
        payload = request.get_json()
        _JSON['key'] = payload['key']
        _JSON['value'] = payload['value']
        _JSON['command'] += f" {payload['key']}/{payload['value']}"
    except:
        _JSON['error'] = "Missing or malformed JSON in client request."
        return jsonify(_JSON), 400

    # Attempt to connect to redis storage layer
    try:
        test_value = r.get(_JSON['key'])
    except RedisError:
        _JSON['error'] = "Cannot connect to redis."
        return jsonify(_JSON), 400

    # POST
    if request.method == 'POST' and not test_value == None:
        _JSON['error'] = "Cannot create new record: key already exists."
        return jsonify(_JSON), 409

    # PUT
    elif (request.method == 'PUT' and test_value == None):
        _JSON['error'] = "Cannot update record: key does not exist."
        return jsonify(_JSON), 404

    # If data is good to send to server, set json data in storage layer to the user inputted data
    else:
        if r.set(_JSON['key'], _JSON['value']) == False:
            _JSON['error'] = "There was a problem creating the value in Redis."
            return jsonify(_JSON), 400
        else:
            _JSON['result'] = True
            return jsonify(_JSON), 200

@app.route('/keyval/<string:key>', methods=['GET', 'DELETE'])
def kv_retrieve(key): # Create a function for the GET and DELETE fucntions
    # Set up json package for the return data
    _JSON = {
        'key': key,
        'value': None,
        'command': "{} {}".format('RETRIEVE' if request.method=='GET' else 'DELETE', key),
        'result': False,
        'error': None
    }
 
    # Attempt to pull data from storage layer.
    try:
        test_value = r.get(key)
    except RedisError:
        _JSON['error'] = "Cannot connect to redis."
        return jsonify(_JSON), 400

    # Need to ensure the data is not an empty field.
    if test_value == '':
        _JSON['error'] = "Key does not exist."
        return jsonify(_JSON), 404
    else:
        _JSON['value'] = test_value
	
    # Fetch the data from the storage layer using GET.
    if request.method == 'GET':
        _JSON['result'] = True
        return jsonify(_JSON), 200

    # Delete data from the storage layer using delete command. Check for proper delete success.
    elif request.method == 'DELETE':
        ret = r.delete(key)
        if ret == 1:
            _JSON['result'] = True
            return jsonify(_JSON)
        else:
            _JSON['error'] = f"Unable to delete key (expected return value 1; client returned {ret})"
            return jsonify(_JSON), 400

# Set app to run @ specified IP and port
if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80)
