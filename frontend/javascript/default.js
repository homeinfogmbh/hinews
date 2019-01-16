$.ajaxPrefilter(function(options, originalOptions, jqXHR) {
	options.crossDomain = {crossDomain: true};
	options.xhrFields = {withCredentials: true};
});

$(document).ready(function() {
	holdSession();
	//$('[data-toggle="tooltip"]').tooltip({html:true});
});  

function getURLParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

function holdSession() {
	$.ajax({
		url: 'https://his.homeinfo.de/session/!?duration=30', //?duration=5 // max 5min - 30min; default: 15min
		type: "PUT",
		success: function (msg) {
			if ((new Date(msg.end) - new Date()) < 0)
				window.location.href = "index.html";
			else {	
				$("#sessiontime").html('<font size="2" color="#bbb">Sitzung läuft ab <br>um ' + msg.end.substring(11, 16) + ' <i class="fa fa-refresh btn_session pointer"></i></font>');
				$('.btn_session').click(function(e) {
					holdSession();
				});
				getUser();
			}
		},
		error: function (msg) { // EXPIRED
			if (msg.statusText == "Gone" ) {
				window.location.href = "index.html"; // Disable for testing without login
			}
		},
	});
}

function getUser() {
	$.ajax({
		timeout: 5000,
		url: "https://his.homeinfo.de/account/!",
		type: "GET",
		success: function (msg) {
			//console.log(msg);
			if (msg.hasOwnProperty('user') && msg.user.hasOwnProperty('first_name'))
				$(".user-name").text(msg.user.first_name + ' ' + msg.user.surname);
			else
				$(".user-name").text(msg.name);
		},
		error: function (msg) {
			console.log('ERROR: default->getUser(): ');
			console.log(msg);
		}
	});	
}

function compareStrings(a, b) {
	try {
		a = a.toString().toLowerCase();
		b = b.toString().toLowerCase();
	} catch(e) {}
	return (a < b) ? -1 : (a > b) ? 1 : 0;
}
function compareStringsInverted(a, b) {
	return (a > b) ? -1 : (a < b) ? 1 : 0;
}