function redirectToHomePage() {
	window.location.replace('/');
}

function redirectToDashboard() {
	window.location.replace('/dashboard');
}

function hasAnAidValue() {
	var aid = localStorage.getItem('aid') || null;
	return null != aid;
}

function setAID(aid) {
	localStorage.setItem('aid', aid)
}

function getAID() {
	return localStorage.getItem('aid')
}
