Vue.component('queue-row', {
	props: ['name', 'inQueueSince'],
	computed: {
		timeSinceInQueue: function(dateString) {
			return moment.utc(dateString).toNow(true);
		}
	},
	template:
	'<tr>' +
		'<td>{{ name }}</td>' +
		'<td>{{ timeSinceInQueue }}</td>' +
		'<td></td>' +
	'</tr>'
});

Vue.component('queue', {
	mounted: function() {
		var self = this;
		ws = new WebSocket(urls.websocket_server_address);

		ws.onopen = function () {
			ws.send(JSON.stringify({
				aid: getAID()
			}));
		};

		ws.onmessage = function (message) {
			try {
				var json = JSON.parse(message.data);
				if (json.request === 'authentication update') {
					ws.send(JSON.stringify({
						request: 'switch_active_group',
						group_id: $.QueryString.group_id
					}))
				} else if (json.request === 'switch active group confirmation') {
					successAlert('Successfully Loaded Group', 1500)
				} else if (json.request === 'queue update') {
					console.log(json.in_queue);
					self.$data.in_queue = json.in_queue;
				}

			} catch (e) {
				console.log('This doesn\'t look like a valid JSON: ', message.data);
			}

		};

		ws.onclose = function () {
			errorAlert('Oh no our connection closed!', 1500);
		};

		$('#join-queue').click(function() {
			ws.send(JSON.stringify({
				request: 'join_queue'
			}));
			successAlert('Joined the Queue', 1500);
		})
	},
	data: function() {
		return {
			in_queue: [
				{
					username: 'bob',
					inQueueSince: '12am'
				}
			]
		}
	},
	template:
	'<div>' +
		'<h3 class="center">Queue</h3>' +
		'<table>' +
			'<thead>' +
				'<tr>' +
					'<th data-field="id">Name</th>' +
					'<th data-field="name">Waiting Since</th>' +
					'<th data-field="price">Rank</th>' +
				'</tr>' +
			'</thead>' +

			'<tbody>' +
				'<queue-row v-for="ticket in in_queue" v-bind:name="ticket.username" v-bind:in-queue-since="ticket.inQueueSince"></queue-row>' +
			'</tbody>' +
		'</table>' +
		'<a id="join-queue">Join Queue</a>' +
	'</div>'
});

Vue.component('group-page', {
	delimiters: ['[[', ']]'],
	mounted: function() {
		var self = this;
		var data = {
			aid: getAID(),
			group_id: $.QueryString.group_id
		};

		$.ajax({
			method: 'POST',
			url: urls.auth_server_address + '/groups/details',
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: 'application/json',
			statusCode: {
				200: function (data) {
					self.$data.group = data.group;
				}
			}
		})
	},
	computed: {
		inviteLink: function () {
			return '/groups/join?invite_code=' + this.$data.group.invite_code;
		}
	},
	template:
	'<div class="row">' +
		'<div class="col l2">' +
			'<h2>[[ group.name ]]</h2>' +
			'<h3>' +
				'<a :href="inviteLink">' +
					'Invite Link' +
				'</a>' +
			'</h3>' +
			'<h3>[[ group.invite_code ]]</h3>' +
		'</div>' +
		'<div class="col l8">' +
			'<queue></queue>' +
		'</div>' +
	'</div>',
	data: function () {
		return {
			group: {
				name: '',
				invite_code: ''
			}
		}
	}
});

function main() {
	var groupPage = new Vue({
		delimiters: ['[[', ']]'],
		el: '#group-page',
		template: '<group-page></group-page>'
	});
}

function onceDocumentReady() {
	getURLs(main);
}

$(document).ready(onceDocumentReady);
