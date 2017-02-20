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
			'<h3 class="center">Queue</h3>' +
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
