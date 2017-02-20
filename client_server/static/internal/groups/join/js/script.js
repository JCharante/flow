function main() {
	var data = {
		aid: getAID(),
		invite_code: $.QueryString.invite_code
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
				}
			}
		})
}

function onceDocumentReady() {
	getURLs(main);
}

$(document).ready(onceDocumentReady);
