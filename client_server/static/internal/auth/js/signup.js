function onceDocumentReady() {
	getURLs(startSubmitButtonListener)
}

function startSubmitButtonListener() {
	$('#submit').click(function () {
		var username = $('#username').val();
		var password = $('#password').val();
		var data = {
			username: username,
			password: password
		};

		$.ajax({
			method: 'POST',
			url: urls.auth_server_address + '/users/join',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: "application/json",
			statusCode: {
				200: function (data) {
					successAlert('Signed Up', 1250);
					console.log('Server Replied: ', data);
					setAID(data.aid);
					redirectToHomePage();
				},
				400: function (responseObject) {
					console.log('Server Replied: ', responseObject);
					data = responseObject.responseJSON;
					switch (data.code) {
						case 4:
							errorAlert('Username Taken', 1250);
							break;
						case 5:
							errorAlert('Insecure Password (Is it blank?)', 1250);
							break;
					}
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);