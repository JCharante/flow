import asyncio
import websockets
import util
import db_functions
import exceptions
from typing import Dict, List


class Group:
	def __init__(self, group_id: str, server: 'QueueWebsocketServer'):
		self.group_id = group_id
		self.server = server
		self.listeners = set()
		self.queue = []  # type: List[QueueTicket]

	def add_listener(self, listener):
		self.listeners.add(listener)

	def remove_listener(self, listener):
		self.listeners.remove(listener)


class QueueTicket:
	def __init__(self, aid: str, group_id: str):
		self.aid = aid
		self.group_id = group_id


class ConnectedClient:
	def __init__(self, socket, server: 'QueueWebsocketServer'):
		self.socket = socket
		self.server = server
		self.aid = None
		self.username = None
		self.authenticated = False
		self.active_group = None

	async def send_json(self, x: dict):
		await self.socket.send(util.dumps(x))

	async def send_error(self, code, message, fields):
		await self.send_json({
			'code': code,
			'message': message,
			'fields': fields
		})

	def set_active_group(self, group_id):
		self.active_group = group_id
		if self.server.groups.get(group_id, None) is None:
			try:
				self.server.initialize_group(group_id)
			except Exception as e:
				print(repr(e))
		group = self.server.groups.get(group_id, None)
		if group is not None:
			group = group  # type: Group
			group.add_listener(self)

	async def on_message(self, message):
		data = util.loads(message)
		if self.authenticated is False:
			aid = data.get('aid', None)
			if aid is None:
				await self.send_error(1, 'Please Identify', 'aid')
				return
			if db_functions.valid_aid(aid):
				self.authenticated = True
				self.aid = aid
				await self.send_json({
					'authenticated': True
				})
				self.server.connected_clients.add(self)
				return
			else:
				await self.send_error(4, 'Invalid AID', 'aid')
				return
		else:
			request = data.get('request', None)
			if request is None:
				await self.send_error(2, 'Requests Must Have A Purpose', 'request')
				return
			if request == 'switch_active_group':
				group_id = data.get('group_id', None)
				if group_id is None:
					await self.send_error(3, 'Required Parameter Missing', 'group_id')
					return
				try:
					is_group_member = db_functions.is_group_member(self.aid, group_id)
				except exceptions.InvalidAid:
					await self.send_error(4, 'You have an invalid aid, wait what?', 'aid')
					return
				except exceptions.InvalidGroupId:
					await self.send_error(5, 'Invalid Group ID', 'group_id')
					return
				else:
					if is_group_member is False:
						await self.send_error(4, 'You are not in this group', 'group_id')
						return
					self.set_active_group(group_id)
					await self.send_json({
						'active_group': self.active_group
					})
					return


class QueueWebsocketServer:
	def __init__(self, port=8883):
		self.groups = {}  # type: Dict[str, Group]
		self.connected_clients = set()
		self.port = port

	def start(self) -> None:
		"""
		Starts the websocket server
		:return:
		"""

		print("Starting Websocket Server on port {}".format(self.port))

		start_server = websockets.serve(self.on_new_connection, 'localhost', self.port)

		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()

	def initialize_group(self, group_id):
		if db_functions.is_valid_group_id(group_id) is False:
			raise exceptions.InvalidGroupId()
		if self.groups.get(group_id, None) is not None:
			raise exceptions.GroupAlreadyInitialized()
		group = Group(group_id, self)
		self.groups[group_id] = group

	async def on_new_connection(self, websocket, path):
		print(f'New Connection | {websocket.remote_address}')
		connected_client = ConnectedClient(websocket, self)
		try:
			while True:
				string = await websocket.recv()
				await connected_client.on_message(string)
		except:
			pass
		finally:
			try:
				self.connected_clients.remove(connected_client)
			except:
				pass
			print(f'Connection Closed | {websocket.remote_address}')

queue_server = QueueWebsocketServer()
queue_server.start()
