function onceDocumentReady() {
	getURLs(startSubmitButtonListener);
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
			url: urls.auth_server_address + '/users/login',
			data: JSON.stringify(data),
			dataType: "json",
			contentType: "application/json",
			statusCode: {
				200: function (data) {
					console.log('Server Replied: ', data);
					Materialize.toast("Logged in", 1250, 'rounded light-green accent-4');
					setAID(data.aid);
					redirectToHomePage();
				},
				400: function (responseObject) {
					console.log('Server Replied: ', responseObject);
					data = responseObject.responseJSON;
					if (data.code == 1) {
						Materialize.toast(data.message, 1250, 'rounded red accent-4');
					}
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);