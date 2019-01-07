checkSession(); // Disable for testing without login

$(document).ready(function() {
	holdSession();
	//$('[data-toggle="tooltip"]').tooltip({html:true});
});  

function getURLParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

function checkSession() {
	$.ajax({
		timeout: 5000,
		url: "https://his.homeinfo.de/session/!?session=" +  localStorage.getItem("token"),
		type: "GET",
		success: function (msg) {
			//console.log(msg);
			//console.log("Success " + msg.token)
			if (msg.token != localStorage.getItem("token")) {
				window.location.href = "index.html";
			} else {
				$("#sessiontime").html('<font size="2" color="#bbb">Sitzung läuft ab <br>um ' + msg.end.substring(11,16) + '</font>');
				getUser();
			}
		},
		error: function (msg) { // EXPIRED
			window.location.href = "index.html";
		}
	});
}
function getUser() {
	$.ajax({
		timeout: 5000,
		url: "https://his.homeinfo.de/account/!?session=" + localStorage.getItem("token"),
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
function holdSession() {
	$.ajax({
		url: "https://his.homeinfo.de/session/!?session=" +  localStorage.getItem("token") + '&duration=30', //?duration=5 // max 5min - 30min; default: 15min
		type: "PUT",
		success: function (msg) {
			localStorage.setItem("token", msg.token);
			$("#sessiontime").html('<font size="2" color="#bbb">Sitzung läuft ab <br>um ' + msg.end.substring(11, 16) + ' <i class="fa fa-refresh btn_session pointer"></i></font>');
			$('.btn_session').click(function(e) {
				holdSession();
			});
		},
		error: function (msg) { // EXPIRED
			if (msg.statusText == "Gone" ) {
				window.location.href = "index.html"; // Disable for testing without login
			}
		},
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