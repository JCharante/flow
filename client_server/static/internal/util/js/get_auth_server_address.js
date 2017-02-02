var urls = null;

function getURLs(callback) {
	if (urls != null) {
		callback();
	}
	$.getJSON('/urls',
		function (data) {
			urls = data;
			callback();
		}
	);
}
