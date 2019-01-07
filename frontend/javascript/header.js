$(document).ready(function() {
	var header = "<nav class='navbar navbar-default'>\
        <a class='navbar-brand' href='start.html'>\
          <img width='81' height='21' class='logo' alt='homeinfo' src='" + (($(location).attr('href').indexOf("charts/") != -1) ?"../" :"") + "img/homeinfologo.png' />\
          <img width='21' height='21' class='logo-xs' alt='homeinfo' src='" + (($(location).attr('href').indexOf("charts/") != -1) ?"../" :"") + "img/homeinfologo.png' />\
        </a>\
        <a class='toggle-nav btn pull-left' href='#'>\
          <i class='fa fa-bars'></i>  \
        </a>\
        <ul class='nav'>\
			<li class='dropdown user-menu'>\
				<a class='dropdown-toggle' data-toggle='dropdown' href='#'>\
				  <span class='user-name'></span>\
				  <b class='caret'></b>\
				</a>\
				<ul class='dropdown-menu'>\
				  <li>\
					<a href='#' class='logout'>\
					  <i class='fa fa-sign-out'></i>\
					  Abmelden\
					</a>\
				  </li>\
				</ul>\
			</li>\
        </ul>\
      </nav>";
	$("#header").html(header);
	
	$('.logout').click(function() {
		$.ajax({
			url: "https://his.homeinfo.de/session/!?session=" +  localStorage.getItem("token"),
			type: "DELETE",
			complete: function (msg) {
				localStorage.removeItem("token");
				window.location.href = "index.html";
			}
		});
	});	
});