checkSession();
$(document).ready(function(){
	$("#warning").hide();
    $("#login").click(function(){
		login();
    });
	if (localStorage.getItem("token") == null)
		$("#container_style").show();
});
$(document).keypress(function(e) {
    if(e.which == 13) { // 'enter'
        login();
    }
});

function login() {
	$('#pageloader').show();
	$.ajax({
		timeout: 3000,
		url: "https://his.homeinfo.de/session", //&duration=5 // max 5min - 30min
		type: "POST",
		contentType: 'application/json',
		data: JSON.stringify({'account':$("#username").val(), "passwd":$("#password").val()}),
		success: function (msg) {
			if (typeof(Storage) !== "undefined") {
				localStorage.setItem("token", msg.token);
				//console.log("Storage TOKEN: " + localStorage.getItem("token"));
				window.location.href = "index.html";
			} else {
				//document.getElementById("warning").innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Dieser Browser unterstützt keine Cookies, dadurch kann die Seite leider nicht benutzt werden.';
				$("#warning").show();
			}
		},
		error: function (msg) {
			try {
				console.log(msg);
				$('#pageloader').hide();
				if (msg.en_US == "Invalid credentials.") {
					document.getElementById("warning").innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> LogIn Daten sind falsch.';
					$("#warning").show();
				} else {
					document.getElementById("warning").innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Leider war der LogIn nicht erfolgreich. Bitte versuchen Sie es später noch einmal.';
					$("#warning").show();					
				}
			} catch(e) {
				document.getElementById("warning").innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Leider war der LogIn nicht erfolgreich. Bitte versuchen Sie es später noch einmal.';
				$("#warning").show();
			}
		}
	});
}

function checkSession() {
	if (localStorage.getItem("token") != null) {
		$('#pageloader').show();
		$.ajax({
			timeout: 3000,
			url: "https://his.homeinfo.de/session/!?session=" +  localStorage.getItem("token"),
			type: "GET",
			success: function (msg) {
				if (msg.token == localStorage.getItem("token")) {
					window.location.href = "index.html";
				}
			},
			error: function (xmlhttprequest, textstatus, message) { // EXPIRED
				$('#pageloader').hide();
				$("#container_style").show();
				if(textstatus === "timeout")
					document.getElementById("warning").innerHTML = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Service ist leider nicht aktiv. Bitte versuchen Sie es später noch einmal.';
			}
		});
	}	
}	