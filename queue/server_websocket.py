import asyncio
import websockets
import util
import db_functions
import exceptions
import datetime
from typing import Dict, List, Set


class Group:
	def __init__(self, group_id: str, server: 'QueueWebsocketServer'):
		self.group_id = group_id
		self.server = server
		self.listeners = set()  # type: Set[ConnectedClient]
		self.queue = []  # type: List[QueueTicket]

	async def add_listener(self, listener):
		self.listeners.add(listener)
		await self.push_queue_update_to_listener(listener)

	def remove_listener(self, listener):
		self.listeners.remove(listener)

	async def join_queue(self, username: str):
		if self.is_in_queue(username) is False:
			self.queue.append(QueueTicket(username, self.group_id))
			await self.push_queue_updates()

	def is_in_queue(self, username: str):
		for ticket in self.queue:
			if ticket.username == username:
				return True
		return False

	async def leave_queue(self, username: str):
		val = None
		for ticket in self.queue:
			if ticket.username == username:
				val = ticket
			break
		self.queue.remove(val)
		await self.push_queue_updates()

	def queue_to_array(self):
		queue = []
		for i in range(len(self.queue)):
			ticket = self.queue[i]
			queue.append({
				'username': ticket.username,
				'inQueueSince': ticket.in_queue_since,
				'position': i + 1
			})
		return queue

	async def push_queue_update_to_listener(self, listener: 'ConnectedClient'):
		message = {
			'request': 'queue update',
			'in_queue': self.queue_to_array()
		}
		await listener.send_json(message)

	async def push_queue_updates(self):
		message = {
			'request': 'queue update',
			'in_queue': self.queue_to_array()
		}
		for listener in self.listeners:
			await listener.send_json(message)


class QueueTicket:
	def __init__(self, username: str, group_id: str):
		self.username = username
		self.group_id = group_id
		self.in_queue_since = datetime.datetime.utcnow().isoformat()


class ConnectedClient:
	def __init__(self, socket, server: 'QueueWebsocketServer'):
		self.socket = socket
		self.server = server
		self.aid = None
		self.username = None
		self.authenticated = False
		self.active_group = None

	async def on_disconnect(self):
		self.active_group.remove_listener(self)
		await self.active_group.leave_queue(self.username)
		self.server.connected_clients.remove(self)

	async def send_json(self, x: dict):
		try:
			await self.socket.send(util.dumps(x))
		except Exception as e:
			print(repr(e))

	async def send_error(self, code, message, fields):
		await self.send_json({
			'code': code,
			'message': message,
			'fields': fields
		})

	async def set_active_group(self, group_id):
		if self.server.groups.get(group_id, None) is None:
			try:
				self.server.initialize_group(group_id)
			except Exception as e:
				print(repr(e))
		group = self.server.groups.get(group_id, None)
		if group is not None:
			self.active_group = group  # type: Group
			await group.add_listener(self)

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
				self.username = db_functions.get_username(aid)
				await self.send_json({
					'request': 'authentication update',
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
					await self.set_active_group(group_id)
					await self.send_json({
						'request': 'switch active group confirmation',
						'active_group': group_id
					})
					return
			elif request == 'join_queue':
				if self.active_group is not None:
					await self.active_group.join_queue(self.username)
			elif request == 'leave_queue':
				if self.active_group is not None:
					await self.active_group.leave_queue(self.username)


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
				await connected_client.on_disconnect()
			except:
				pass
			print(f'Connection Closed | {websocket.remote_address}')

queue_server = QueueWebsocketServer()
queue_server.start()
