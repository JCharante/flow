Vue.component('group', {
	delimiters: ['[[', ']]'],
	props: ['name', 'owner', 'groupId'],
	template:
	'<div class="col s12 m6 l4 group">' +
		'<p>Group Name  : [[ name ]]</p>' +
		'<p>Group Owner : [[ owner ]]</p>' +
		'<p>Group ID    : [[ groupId ]]</p>' +
	'</div>'
});


Vue.component('groups', {
	delimiters: ['[[', ']]'],
	mounted: function() {
		var self = this;
		getURLs(function() {
			$.getJSON(urls.auth_server_address + '/users/' + getAID() + '/groups',
				function (data) {
					/*var alt_data = {
						groups: [
							{
								name: 'TestGroup1',
								owner: 'JCharante',
								group_id: '3rnf2i3rj3'
							},{
								name: 'TestGroup2',
								owner: 'JCharante',
								group_id: '313123123'
							}
						]
					};*/
					self.$data.groups = data.groups;
				}
			);
		});
	},
	template: '<div id="groups" class="row"><group v-for="group in groups" v-bind:name="group.name" v-bind:owner="group.owner" v-bind:group-id="group.group_id"></group></div>',
	data: function () {
		return {
			groups: []
		}
	}
});

new Vue({
	delimiters: ['[[', ']]'],
	el: '#groups-div'
});
