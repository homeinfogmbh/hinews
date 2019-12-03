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
			var promises = [];
			promises.push(getArticleList());
			promises.push(getArticleList("&inactive"));
			Promise.all(promises).then(getArticleListCompleted);
	
		},
		error: function (msg) {
			console.log(msg);
		}
	});	
}

function getArticleListCompleted(data) {
	var activityData = [];
	var activity = '';
	var article;
	var editor;
	for (article = 0; article < data[0].length; article++) {
		activityData.push({'id':data[0][article].id, 'user':data[0][article].author.id, 'date':data[0][article].created, 'activity':'News <b>"' + data[0][article].title + '"</b> erstellt'});
		for (editor = 0; editor < data[0][article].editors.length; editor++)
			activityData.push({'id':data[0][article].id, 'user':data[0][article].editors[editor].account.id, 'date':data[0][article].editors[editor].timestamp, 'activity':'News <b>"' + data[1][article].title + '"</b> bearbeitet'});
	}
	for (article = 0; article < data[1].length; article++) {
		activityData.push({'id':data[1][article].id, 'user':data[1][article].author.id, 'date':data[1][article].created, 'activity':'News <b>"' + data[1][article].title + '"</b> erstellt'});
		for (editor = 0; editor < data[1][article].editors.length; editor++)
			activityData.push({'id':data[1][article].id, 'user':data[1][article].editors[editor].account.id, 'date':data[1][article].editors[editor].timestamp, 'activity':'News <b>"' + data[1][article].title + '"</b> bearbeitet'});
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
	$('#pageloader').hide();
}
function getArticleList(active = "") {
	$.ajax({
		url: "https://backend.homeinfo.de/hinews/article" + active,
		type: "GET",
		success: function (articles) { },
		error: function (msg) {
			JSON.stringify(msg);
			console.log(msg);
		}
	});
}