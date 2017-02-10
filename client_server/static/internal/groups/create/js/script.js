function onceDocumentReady() {
	getURLs(startSubmitButtonListener);
}

function startSubmitButtonListener() {
	$('#submit').click(function () {
		var group_name = $('#group_name').val();
		var aid = getAID();
		var data = {
			group_name: group_name,
			aid: aid
		};

		$.ajax({
			method: 'POST',
			url: urls.auth_server_address + '/groups/create',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: "application/json",
			statusCode: {
				200: function (data) {
					console.log('Server Replied: ', data);
					Materialize.toast('Created Group!', 420, 'light-green accent-4');
					redirectToDashboard();
				},
				400: function (responseObject) {
					console.log('Server Replied: ', responseObject);
					data = responseObject.responseJSON;
					Materialize.toast(data.message + '\n' + data.fields + '\n', data.code, 3000, 'red accent-4');
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);