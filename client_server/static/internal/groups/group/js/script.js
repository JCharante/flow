Vue.component('queue-row', {
	props: ['name', 'inQueueSince', 'position'],
	mounted: function() {
		var self = this;

        setInterval(function() {
            self.$data.timeSinceInQueue = moment.utc(self.inQueueSince).toNow(true) + ' ago';
        }, 1000);
	},
	data: function() {
		return {
			timeSinceInQueue: 'just now'
		}
	},
	template:
	'<tr>' +
		'<td>{{ name }}</td>' +
		'<td>{{ timeSinceInQueue }}</td>' +
		'<td>#{{ position }}</td>' +
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
				} else {
					console.log(json);
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
		});

		var queueToggle = $('#queueToggle');

		queueToggle.click(function() {
			var text = queueToggle.text();
			if (text === 'Leave Queue') {
				ws.send(JSON.stringify({
					request: 'leave_queue'
				}));
				queueToggle.removeClass('in-queue');
				queueToggle.addClass('out-of-queue');
				queueToggle.text('Join Queue');
			} else if (text === 'Join Queue') {
				ws.send(JSON.stringify({
					request: 'join_queue'
				}));
				queueToggle.removeClass('out-of-queue');
				queueToggle.addClass('in-queue');
				queueToggle.text('Leave Queue');
			}
		})
	},
	data: function() {
		return {
			in_queue: []
		}
	},
	template:
	'<div>' +
		'<h3 class="center">Queue</h3>' +
		'<table>' +
			'<thead>' +
				'<tr>' +
					'<th data-field="id">Name</th>' +
					'<th data-field="name">Joined the Queue</th>' +
					'<th data-field="price">Place in Line</th>' +
				'</tr>' +
			'</thead>' +

			'<tbody>' +
				'<queue-row v-for="ticket in in_queue" :position="ticket.position" v-bind:name="ticket.username" v-bind:in-queue-since="ticket.inQueueSince"></queue-row>' +
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
		'<div class="col l7">' +
			'<queue></queue>' +
		'</div>' +
		'<div class="col l1">' +
			'<div id="queueToggle" class="out-of-queue">Join Queue</div>' +
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
