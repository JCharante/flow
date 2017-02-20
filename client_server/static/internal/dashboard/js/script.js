Vue.component('group', {
	delimiters: ['[[', ']]'],
	props: ['name', 'owner', 'groupId'],
	computed: {
		groupPageLink: function () {
			return '/groups/group?group_id=' + this.groupId;
		}
	},
	template:
	'<div class="col s12 m6 l4 group">' +
		'<h3 class="center"><a :href="[[ groupPageLink ]]">[[ name ]]</h3>' +
		'<p>Group Owner : [[ owner ]]</p>' +
		'<p>Group ID    : [[ groupId ]]</p>' +
	'</div>'
});


Vue.component('groups', {
	delimiters: ['[[', ']]'],
	mounted: function() {
		var self = this;
		getURLs(function() {
			var data = {
				aid: getAID()
			};

			$.ajax({
				method: 'POST',
				url: urls.auth_server_address + '/users/groups',
				data: JSON.stringify(data),
				dataType: "json",
				contentType: "application/json",
				statusCode: {
					200: function (data) {
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
				}
			});
		});
	},
	template: '<div id="groups" class="row">' +
	'<group v-for="group in groups" v-bind:name="group.name" v-bind:owner="group.owner" v-bind:group-id="group.group_id"></group>' +
	'</div>',
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
