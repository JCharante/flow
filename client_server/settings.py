import json
import util


class Settings:
	def __init__(self):
		self.settings = {}
		self.read_settings()

		self.auth_server_address = self.settings.get('auth_server_address', '')
		self.websocket_server_address = self.settings.get('websocket_server_address', '')

	def read_settings(self):
		with open(util.path_to_this_files_directory() + 'settings.json') as json_data:
			self.settings = json.load(json_data)
