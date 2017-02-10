from flask import Flask, request, jsonify, make_response, abort, Response, render_template
from settings import Settings
import util

app = Flask(__name__)
settings = Settings()


def home_cor(obj):
	return_response = make_response(obj)
	return_response.headers['Access-Control-Allow-Origin'] = "*"
	return_response.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
	return_response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Origin, Accept"
	return return_response


@app.route('/')
def landing():
	return render_template('landing/index.html')


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard/dashboard.html')


@app.route('/groups/create')
def groups_create():
	return render_template('groups/create.html')


@app.route('/auth/login')
def auth_login():
	return render_template('auth/login.html')


@app.route('/auth/signup')
def auth_signup():
	return render_template('auth/signup.html')


@app.route('/auth/logout')
def auth_logout():
	return render_template('auth/logout.html')


@app.route('/version', methods=['GET', 'OPTIONS'])
def version():
	if request.method == 'OPTIONS':
		return home_cor(jsonify(**{}))
	elif request.method == 'GET':
		return home_cor(jsonify(**{
			"git_version": util.get_git_revision_short_hash()
		}))


@app.route('/urls')
def urls():
	return home_cor(jsonify(**{
		'auth_server_address': settings.auth_server_address
	}))


app.run(debug=True, host='0.0.0.0', port=8882, threaded=True)
