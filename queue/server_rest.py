from flask import Flask, request, jsonify, make_response, abort, Response, url_for
import db_functions
import config
import util
import exceptions
from settings import Settings
import json

app = Flask(__name__)

settings = Settings()


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


@app.errorhandler(400)
def http_400(code, message, fields):
	response_object = home_cor(Response(json.dumps({
		'code': code,
		'message': message,
		'fields': fields
	}), 400))
	response_object.headers['Content-Type'] = 'application/json'
	return response_object


@app.route('/', methods=['OPTIONS', 'GET'])
def root():
	if request.method == 'GET':
		response = {
			'endpoints': {
				'users': settings.public_address + '/users/aid_here',
				'groups': settings.public_address + '/groups/group_id'
			}
		}
		return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))


@app.route('/groups/<group_id>')
def groups(group_id: str):
	response = {
		'create': settings.public_address + '/groups/create?aid=aid_here&name=group_name',
		'invite_code': settings.public_address + '/groups/group_id/invite_code'
	}
	return home_cor(jsonify(**response))


@app.route('/groups/create', methods=['OPTIONS', 'GET'])
def groups_create():
	if request.method == 'GET':
		response = {}
		name = request.args.get('name', '')
		aid = request.args.get('aid', '')
		try:
			group_id = db_functions.create_group(aid, name)
		except exceptions.InvalidAid:
			return http_401('Invalid AID')
		else:
			response['group_id'] = group_id
		return home_cor(jsonify(**response))
	elif request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))


@app.route('/groups/join/<invite_code>', methods=['OPTIONS', 'GET'])
def groups_join(invite_code):
	if request.method == 'GET':
		response = {}
		aid = request.args.get('aid', '')
		try:
			db_functions.join_group_through_invite_link(aid, invite_code)
		except exceptions.InvalidAid:
			return http_401('Invalid AID')
		except exceptions.InvalidGroupInviteCode:
			return http_401('Invalid Invite Code')
		else:
			response['success'] = True
		return home_cor(jsonify(**response))
	elif request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))


@app.route('/groups/<group_id>/invite_code', methods=['OPTIONS', 'GET'])
def groups_group_id(group_id):
	if request.method == 'GET':
		response = {}
		try:
			invite_code = db_functions.get_invite_code(group_id)
		except exceptions.InvalidGroupId:
			return http_401('Invalid Group ID')
		else:
			response['success'] = True
			response['invite_code'] = invite_code
		return home_cor(jsonify(**response))
	elif request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))

"""
@app.route('/users/<aid>', methods=['OPTIONS', 'GET'])
def users(aid: str):
	if request.method == 'GET':
		response = {
			'endpoints': {
				'username': settings.public_address + f'/users/{aid}/username',
				'last_login': settings.public_address + f'/users/{aid}/last_login',
				'join': settings.public_address + '/users/join?username=UsernameHere&password=PasswordHere',
				'login': settings.public_address + '/users/login?username=UsernameHere&password=PasswordHere',
				'metrics': settings.public_address + '/users/metrics'
			}
		}
		if settings.dev_mode:
			response['endpoints']['wipe_users'] = settings.public_address + '/users/wipe'
		return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))
"""


@app.route('/users/join', methods=['POST', 'OPTIONS', 'GET'])
def users_join():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	username = None
	password = None

	if request.method == 'GET':
		username = request.args.get('username', None)
		password = request.args.get('password', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if username is None:
		return http_400(3, 'Required Parameter is Missing', 'username')
	if password is None:
		return http_400(3, 'Required Parameter is Missing', 'password')

	try:
		aid = db_functions.create_user(username, password)
	except exceptions.UsernameNotUniqueException:
		return http_400(4, 'Username Taken', 'username')
	except exceptions.InsecurePasswordException:
		return http_400(5, 'Password Is Too Weak', 'password')

	response['aid'] = aid
	return home_cor(jsonify(**response))


@app.route('/users/login', methods=['POST', 'OPTIONS', 'GET'])
def users_login():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	username = None
	password = None

	if request.method == 'GET':
		username = request.args.get('username', None)
		password = request.args.get('password', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			username = data.get('username', None)
			password = data.get('password', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if username is None:
		return http_400(3, 'Required Parameter is Missing', 'username')
	if password is None:
		return http_400(3, 'Required Parameter is Missing', 'password')

	try:
		aid = db_functions.login(username, password)
	except exceptions.InvalidCredentials:
		return http_400(1, 'Invalid Credentials', 'Username/Password')

	response['aid'] = aid
	return home_cor(jsonify(**response))


@app.route('/users/wipe')
def users_wipe():
	if settings.dev_mode:
		db_functions.wipe_users()
		return home_cor(jsonify(**{
			'success': True
		}))
	else:
		return home_cor(jsonify(**{
			'success': False,
			'error': 'not running in dev mode'
		}))


@app.route('/users/metrics')
def users_quantity():
	return home_cor(jsonify(**{
		'RegisteredUsers': db_functions.number_of_users()
	}))


@app.route('/users/username', methods=['OPTIONS', 'GET', 'POST'])
def users_username():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	aid = aid  # type: str
	try:
		username = db_functions.get_username(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['username'] = username
	return home_cor(jsonify(**response))


@app.route('/users/last_login', methods=['OPTIONS', 'GET', 'POST'])
def users_last_login():
	response = dict()

	if request.method == 'OPTIONS':
		return home_cor(jsonify(**response))

	aid = None

	if request.method == 'GET':
		aid = request.args.get('aid', None)
	elif request.method == 'POST':
		data = request.json
		if data is not None:
			aid = data.get('aid', None)
		else:
			return http_400(2, 'Required JSON Object Not Sent', 'body')

	if aid is None:
		return http_400(3, 'Required Parameter is Missing', 'aid')

	aid = aid  # type: str
	try:
		last_login = db_functions.get_last_login(aid)
	except exceptions.InvalidAid:
		return http_400(6, 'Invalid AID', 'aid')

	response['last_login'] = last_login
	return home_cor(jsonify(**response))


@app.route('/users/<aid>/groups', methods=['OPTIONS', 'GET'])
def users_aid_groups(aid: str):
	if request.method == 'GET':
		response = {}
		try:
			groups = db_functions.groups_user_is_in(aid)
		except exceptions.InvalidAid:
			return http_401('Invalid AID')
		else:
			response['groups'] = groups
		return home_cor(jsonify(**response))
	else:
		return home_cor(jsonify(**{}))


print(f'Using Database: {config.path_to_db}')

app.run(debug=True, host='0.0.0.0', port=8881)
