$(document).ready(function() {
	var previous = ($(location).attr('href').indexOf("charts/") != -1) ?"../" :"";
	var menue = "<div class='loader' id='pageloader'>\
		</div><nav id='main-nav'>\
			<div class='navigation'>\
			  <div class='search'>\
				<form action='search_results.html' method='get'>\
				  <div class='search-wrapper'>\
					<input type='text' name='q' value='' class='search-query form-control' placeholder='Suche...' autocomplete='off' />\
					<button class='btn btn-link fa fa-search' name='button' type='submit'></button>\
				  </div>\
				</form>\
			  </div>\
			  <ul class='nav nav-stacked'>\
				<li class='" + (($(location).attr('href').indexOf("start.html") != -1) ?"active" :"") + "'>\
				<a href='" + previous + "start.html'>\
					<i class='fa fa-dot-circle-o'></i>\
					<span>Start</span>\
				  </a>\
				</li>\
				<li class='" + (($(location).attr('href').indexOf("article.html") != -1) ?"active" :"") + "'>\
				<a href='" + previous + "article.html'>\
					<i class='fa fa-cubes'></i>\
					<span>News anlegen</span>\
				  </a>\
				</li>\
				<li class='" + (($(location).attr('href').indexOf("manage.html") != -1) ?"active" :"") + "'>\
				<a href='" + previous + "manage.html'>\
					<i class='fa fa-cogs'></i>\
					<span>News verwalten</span>\
				  </a>\
				</li>\
				<li class='" + (($(location).attr('href').indexOf("overview.html") != -1) ?"active" :"") + "'>\
				<a href='" + previous + "overview.html'>\
					<i class='fa fa-cogs'></i>\
					<span>Kundenzuordnung</span>\
				  </a>\
				</li>\
			  </ul>\
			</div><br><br>\
			<div id='sessiontime' style='margin-left:20%;'>\
			</div>\
		  </nav>";
	$("#menue").html(menue);
});