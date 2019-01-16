$('#pageloader').show();
var _articles = []; // JSON from backend
var _customers;
$(document).ready(function() {
	getCustomers();
	$('#searchfield').on('input',function(e) {
		loadArticles();
	});	
});

function getCustomers() {
	$.ajax({
		url: 'https://backend.homeinfo.de/hinews/customers',
		type: 'GET',
		success: function (customers) {
			console.log(customers);
			_customers = customers;
			getArticleList();
		},
		error: function (msg) {
			console.log(msg);
		}
	});
}
function getArticleList() {
	$.ajax({
		url: 'https://backend.homeinfo.de/hinews/article',
		type: "GET",
		success: function (articles) {
			console.log(articles)
			_articles = articles;
			for (var article = 0; article < _articles.length; article++) {
				if (_articles[article].editors.length > 0)
					_articles[article].created = _articles[article].editors[_articles[article].editors.length-1].timestamp;
			}
			_articles.sort(function(a, b) {
				return compareStringsInverted(a.created, b.created);
			})
			loadArticles();
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

function loadArticles() {
	var newslist = '';
	var tags;
	var datecolor;
	var counter = 0;
	var header = "<th class='sticky'>Titel</th>";
	var found;
	for (var customer = 0; customer < _customers.length; customer++)
		header += "<th>" + _customers[customer].company.name + "(" + _customers[customer].cid + ")</th>";
	for (var i = 0; i < _articles.length; i++) {
		if (search(i) && ($('#keywords').text() === 'keine' || searchTags(i))) {
			//tags = '';
			datecolor = '';
			//for (var tag = 0; tag < _articles[i].tags.length; tag++)
				//tags += _articles[i].tags[tag].tag + ((tag < _articles[i].tags.length-1) ?', ' :'');
			if (new Date() < new Date(_articles[i].active_from) || (new Date() > new Date(_articles[i].active_until).setHours(23,59,59,999) && _articles[i].active_until !== null)) // SetHours of end of day
				datecolor = "style='background-color:#ffc7c7'";
			newslist += "<tr " + datecolor + ">" + 
					"<td class='sticky'>" + _articles[i].title + "</td>";
					
			for (var customer = 0; customer < _customers.length; customer++) {
				found = false;
				for (var article = 0; article < _articles[i].customers.length; article++) {
					if (_customers[customer].cid == _articles[i].customers[article].customer) {
						found = true;
						break;
					}
				}
				if (_articles[i].customers.length === 0)
					found = true;
				else {
				}
				if (found)
					newslist +=  '<td>X</td>';
				else 
					newslist +=  '<td></td>';
			}
			newslist += "</tr>";
		}
	}
	$('#customerlist').html(header);
	$('#newslist').html(newslist);
	setButtons();
	$('[data-toggle="tooltip"]').tooltip({html:true});	
}
function setButtons() {
	$('.btn_removekeyword').unbind();
	$('.btn_removekeyword').click(function(e) {
		$(this).remove();
		setKeywordSelections();
		loadArticles();
	});
	$('.btn_edit_news').click(function(e) {
		window.location.href = "article.html?id=" + $(this).data('jsonid');
	});
	
	$('.btn_delete').click(function(e) {
		if ($(this).text() === 'nein') {
			$(this).parent().hide('fast');
		} else {
			if ($(this).parent().find('.confirm').is(":visible"))
				$(this).parent().find('.confirm').hide('fast')
			else
				$(this).parent().find('.confirm').show('fast');
		}
		e.preventDefault();
	});
	$('.btn_delete_news').click(function(e) {
		var id = _articles[$(this).data('jsonid')].id;
		var title = _articles[$(this).data('jsonid')].title;
		$("#pageloader").show();
		//for (i=0; i < msg.length; i++) { // delete all // multi
		$.ajax({
			url: 'https://backend.homeinfo.de/hinews/article/" + id',
			type: "DELETE",
			success: function (msg) {
				//console.log(msg);
				$("#message").html('<font size="4" color="#FF0000">Die News "' + ((title === '') ?"ohne Titel" :title) + '" wurde gelöscht.</font>');
				getArticleList();
			},
			error: function (msg) {
				$("#pageloader").hide();
				console.log(msg);
				$("#message").html('<font size="4" color="#FF0000">Beim Löschen der News ' + ((title === '') ?"ohne Titel" :title) + ' ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.</font>');
			}
		});
		//}
		e.preventDefault();
	});	
}
function search(nr) {
	try {
		if ($('#searchfield').val().trim() == '')
			return true;
		else if (_articles[nr].title.toString().toLowerCase().indexOf($('#searchfield').val().toLowerCase()) !== -1)
			return true;
		else if (_articles[nr].text.toString().toLowerCase().indexOf($('#searchfield').val().toLowerCase()) !== -1)
			return true;
		else if (_articles[nr].subtitle.toString().toLowerCase().indexOf($('#searchfield').val().toLowerCase()) !== -1)
			return true;
	} catch (e) { }
	return false;
}
function setKeywordSelections() {
	var selection = '';
	var allowSelection;
	for (keyword in _keywords) {
		allowSelection = true;
		for (var selectedKeyword = 0; selectedKeyword < $('#keywords').find('span').length; selectedKeyword++) {
			if ($('#keywords').find('span').eq(selectedKeyword).text() === _keywords[keyword]) {
				allowSelection = false;
				break;
			}
		}
		if (allowSelection)
			selection += '<option>' + _keywords[keyword] + '</option>';
		$('#keyword').html(selection);
	}
	if ($('#keywords').text() === '')
		$('#keywords').html('keine');
}
function searchTags(nr) {
	var keywordfound;
	for (var selectedKeyword = 0; selectedKeyword < $('#keywords').find('span').length; selectedKeyword++) {
		keywordfound = false;
		for (var tag = 0; tag < _articles[nr].tags.length; tag++) {
			if ($('#keywords').find('span').eq(selectedKeyword).text() === _articles[nr].tags[tag].tag)
				keywordfound = true;
		}
		if (!keywordfound)
			return false;
	}
	return true;
}