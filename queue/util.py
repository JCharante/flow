import bcrypt
import os
import random
import json


def encrypt_new_password(password):
	one_time_use_salt = bcrypt.gensalt()
	encrypted_password = bcrypt.hashpw(password.encode('utf-8'), one_time_use_salt)
	return encrypted_password


def path_to_this_files_directory():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	return dir_path + '/'


def checkpw(stored_password, entered_password):
	return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))


def secure_password(password):
	return len(password) > 0


def generate_alphanumeric_string(length):
	return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(length))


def loads(x: str):
	try:
		return json.loads(x)
	except:
		return {}


def dumps(x: dict):
	try:
		return json.dumps(x)
	except:
		return "{}"
