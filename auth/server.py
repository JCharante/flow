from flask import Flask, request, jsonify, make_response, abort, Response, url_for
import db_functions
import config
import util
import exceptions
import json

app = Flask(__name__)

public_address = json.load(open(util.path_to_this_files_directory() + 'settings.json')).get('public_address', '')


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


@app.errorhandler(401)
def http_401(message=''):
	if message == '':
		return home_cor(Response('Invalid Credentials', 401, {'Erebus': 'error="Invalid Credentials"'}))
	else:
		return home_cor(Response(message, 401))


@app.route('/', methods=['OPTIONS', 'GET'])
def root():
	if request.method == 'GET':
		response = {
			'endpoints': {
				'users': public_address + url_for('users', aid='aid_here'),
			}
		}
		return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))


@app.route('/users/<aid>', methods=['OPTIONS', 'GET'])
def users(aid: str):
	if request.method == 'GET':
		response = {
			'endpoints': {
				'username': public_address + '/users/<aid>/username',
				'last_login': public_address + '/users/<aid>/last_login',
				'join': public_address + '/users/join?username=UsernameHere&password=PasswordHere',
				'login': public_address + '/users/login?username=UsernameHere&password=PasswordHere'
			}
		}
		return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))


@app.route('/users/join', methods=['POST', 'OPTIONS', 'GET'])
def users_join():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	elif request.method == 'GET':
		username = request.args.get('username', '')
		password = request.args.get('password', '')

		try:
			db_response = db_functions.create_user(username, password)
		except exceptions.UsernameNotUniqueException:
			return http_401('Username Taken.')
		except exceptions.InsecurePasswordException:
			return http_401('Insecure Password Used')
		else:
			if db_response[0]:
				response['status'] = 'Success'
				response['uid'] = db_response[1]
				return home_cor(jsonify(**response))
			else:
				return http_401('Username Taken.')
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
			if username is not None and password is not None:
				db_response = db_functions.create_user(username, password)
				if db_response[0]:
					response['status'] = 'Success'
					response['uid'] = db_response[1]
					return home_cor(jsonify(**response))
		return http_401()


@app.route('/users/login', methods=['POST', 'OPTIONS', 'GET'])
def users_login():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))
	elif request.method == 'GET':
		username = request.args.get('username', '')
		password = request.args.get('password', '')
		aid = db_functions.login(username, password)
		response['valid_aid'] = aid[0]
		response['aid'] = aid[1]
		return home_cor(jsonify(**response))
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
			if username is not None and password is not None:
				db_response = db_functions.login(username, password)
				if db_response[0]:
					response['status'] = 'Success'
					response['uid'] = db_response[1]
					return home_cor(jsonify(**response))
		return http_401()


@app.route('/users/<aid>/username', methods=['OPTIONS', 'GET'])
def users_username(aid: str):
	if request.method == 'GET':
		response = {}
		try:
			username = db_functions.get_username(aid)
		except exceptions.InvalidAid:
			response['valid_aid'] = False
		else:
			response['valid_aid'] = True
			response['username'] = username
		finally:
			return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))


@app.route('/users/<aid>/last_login', methods=['OPTIONS', 'GET'])
def users_last_login(aid: str):
	if request.method == 'GET':
		response = {}
		try:
			last_login = db_functions.get_last_login(aid)
		except exceptions.InvalidAid:
			response['valid_aid'] = False
		else:
			response['last_login'] = last_login
			response['valid_aid'] = True
		finally:
			return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))

print(f'Database file located at: {config.path_to_db}')

app.run(debug=True, host='0.0.0.0', port=3234)