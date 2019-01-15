var _customers;
var _newsAllowedCount = {'993301':2,'1030001':2,'1030019':2,'1030020':2,'1031001':2,'1031002':2,'1038003':2,'1038007':2,'1044003':2,'1049002':2,'1049003':2,'2047001':2,'2059001':2,'2070001':2,'3033001':2};
var _users;
$(document).ready(function() {
	getCustomers();
});

function getCustomers() {
	$.ajax({
		url: 'https://backend.homeinfo.de/hinews/customers',
		type: 'GET',
		success: function (customers) {
			//console.log(customers);
			_customers = customers;
			getUserList();
		},
		error: function (msg) {
			console.log(msg);
		}
	});
}
function getUserList() {
	$.ajax({
		timeout: 5000,
		url: 'https://his.homeinfo.de/account/!',
		type: "GET",
		success: function (users) {
			_users = users;
			getActives();
		},
		error: function (msg) {
			console.log(msg);
		}
	});	
}
function getActives() {
	$.ajax({
		timeout: 5000,
		url: "https://backend.homeinfo.de/hinews/articles",
		type: "GET",
		success: function (actives) {
			var overview = 'Aktive News: <b>' + actives.active + '</b><br>' +
					'News gesamt: <b>' + ( actives.active + actives.inactive) + '</b><br><br>';
			$('#overview').html(overview);
			getArticleList();
		},
		error: function (msg) {
			console.log(msg);
		}
	});	
}
function getArticleList() {
	$.ajax({
		url: "https://backend.homeinfo.de/hinews/article",
		type: "GET",
		success: function (articles) {
			var activityData = [];
			var activity = '';
			for (var article = 0; article < articles.length; article++) {
				activityData.push({'id':articles[article].id, 'user':articles[article].author.id, 'date':articles[article].created, 'activity':'News <b>"' + articles[article].title + '"</b> erstellt'}); // $.datepicker.formatDate('mm/dd/yy', new Date(articles[article].created))
				for (var editor = 0; editor < articles[article].editors.length; editor++)
					activityData.push({'id':articles[article].id, 'user':articles[article].editors[editor].account.id, 'date':articles[article].editors[editor].timestamp, 'activity':'News <b>"' + articles[article].title + '"</b> bearbeitet'}); // $.datepicker.formatDate('mm/dd/yy', new Date(articles[article].created))
			}
			activityData.sort(function(a, b) {
				return compareStringsInverted(a.date, b.date);
			})
			var user;
			for (var i = 0; i < ((activityData.length > 100) ?100 :activityData.length); i++) {
				activity += "<tr>" + 
						"<td>" + (i+1) + "</td>" +
						"<td>" + activityData[i].id + "</td>" +
						"<td>" + activityData[i].user + "</td>" +
						"<td>" + activityData[i].activity + "</td>" +
						"<td>" + activityData[i].date.split('T').join(' ') + "</td>" +
					"</tr>"
			}
			$('#activity').html(activity);
		},
		complete: function (msg) {
			$('#pageloader').hide();
		},
		error: function (msg) {
			JSON.stringify(msg);
			console.log(msg);
		}
	});
}