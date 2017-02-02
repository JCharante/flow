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
			success: function (data) {
				if (data['status'] == 'Success') {
					Materialize.toast("Logged in", 2000, 'rounded light-green accent-4');
					setAID(data['aid']);
					redirectToHomePage();
				} else {
					console.log(data);
				}
			},
			error: function (jqXHR, exception) {
				if (jqXHR.status === 401) {
					Materialize.toast('Invalid Credentials (Username Taken or Password is Blank)', 1500, 'rounded red accent-4');
				} else {
					Materialize.toast('flow May Be Down Right Now :(', 1500, 'rounded red accent-4');
					console.log('Unknown Error. \n ' + jqXHR.responseText);
				}
			}
		});
	});
}

$(document).ready(onceDocumentReady);