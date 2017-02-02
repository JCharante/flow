$(document).ready(function() {
	$('.button-collapse').sideNav();
	$('.dropdown-button').dropdown();
	populateAccountDropDownMenu();
});

function populateAccountDropDownMenu() {
	if (hasAnAidValue()) {
		addLogOutButton();
	} else {
		addLoginButton();
		addRegisterButton();
	}
}

function addLogOutButton() {
	$('#dropdown1').append('<li><a href="/auth/logout">Logout</a>');
}

function addLoginButton() {
	$('#dropdown1').append('<li><a href="/auth/login">Login</a>');
}

function addRegisterButton() {
	$('#dropdown1').append('<li><a href="/auth/signup">Signup</a>');
}

function getURLs(callback) {
	$.getJSON('/urls',
		function (data) {
			console.log("Cynosural: ", "URLs: ", data);
			callback(data);
		}
	);
}
