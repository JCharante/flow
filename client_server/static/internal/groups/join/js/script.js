function main() {

	if ($.QueryString.invite_code != null) {
		joinGroup($.QueryString.invite_code)
	} else {
		$('#submit').click(function() {
			joinGroup($('#invite_code').val())
		})
	}
}

function joinGroup(invite_code) {
	var data = {
		aid: getAID(),
		invite_code: invite_code
	};

	$.ajax({
		method: 'POST',
		url: urls.auth_server_address + '/groups/join',
		data: JSON.stringify(data),
		dataType: 'json',
		contentType: 'application/json',
		statusCode: {
			200: function (data) {
				redirectToDashboard()
			},
			400: function (data) {
				redirectToDashboard()
			}
		}
	})
}

function onceDocumentReady() {
	getURLs(main);
}

$(document).ready(onceDocumentReady);
