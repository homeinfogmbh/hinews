var _articles = []; // JSON from backend
var _keywords;
var _companies;
var _selectedPage = 0;
var _showactive = true;
$(document).ready(function() {
	 $("#actives").val('true');
	getPages(); // getKeywords();
	$('#searchfield').on('input',function(e) {
		loadArticles();
	});

	$('.keywords').click(function(e) {
		if ($(this).val() !== null) {
			var selector;
			if ($(this)[0].id === 'company')
				selector = $('#companies');
			else
				selector = $('#keywords');

			if (selector.text() === 'keine' || selector.text() === 'alle')
				selector.empty();
			selector.append("<span class='label label-default btn_removekeyword pointer' style='margin-right:5px; display: inline-block' data-cid=" + $(this).find(':selected').data('cid') + ">" + $(this).val() + "<i class='fa fa-times' style='margin-left:5px'></i></span>");
			$('option:selected', this).remove();
			loadArticles();
		}
	});

	$("#actives").change(function() {
		$("#pageloader").show();
		_showactive = $(this).val() == 'true' ?true :false;
		getPages();
	});
});

function getKeywords() {
	$.ajax({
		url: 'https://backend.homeinfo.de/hinews/customers',
		type: 'GET',
		success: function (companies) {
			_companies = companies;
			_companies.sort(function(a, b) {
				return compareStrings(a.id, b.id);
			})
			$.ajax({
				url: 'https://backend.homeinfo.de/hinews/tags',
				type: 'GET',
				success: function (tags) {
					_keywords = tags;
					_keywords.sort(function(a, b) {
						return compareStrings(a, b);
					});
					setKeywordSelections();
					getPages();
				},
				error: function (msg) {
					console.log(msg);
				}
			});
		},
		error: function (msg) {
			console.log(msg);
		}
	});
}
function getPages() {
	$.ajax({
		url: "https://backend.homeinfo.de/hinews/article?pages&size=15" + (_showactive ?"" :"&inactive"),
		type: "GET",
		success: function (pages) {
			if (pages.pages > 1) {
				var pagechanger = '';
				for (var i = 0; i < pages.pages; i++)
					pagechanger += '<a href="#" class="pagechanger" data-page="' + i + '" title="Seite ' + (i+1) + '"><u>' + (i+1) + '</u></a> ';
				$('#pages').html(pagechanger);
			}
			getArticleList();
		},
		error: function (msg) {
			console.log(msg);
		}
	});
}
function getArticleList() {
	$.ajax({
		url: "https://backend.homeinfo.de/hinews/article?size=15&page=" + _selectedPage + (_showactive ?"" :"&inactive"),
		type: "GET",
		success: function (articles) {
			_articles = articles;
			for (var article = 0; article < _articles.length; article++) {
				if (_articles[article].editors.length > 0)
					_articles[article].created = _articles[article].editors[_articles[article].editors.length-1].timestamp;
			}
			_articles.sort(function(a, b) {
				return compareStringsInverted(a.created, b.created);
			})
			loadArticles(true);
		},
		complete: function (msg) {
			$('#pageloader').hide();
		},
		error: function (msg) {
			console.log(msg);
		}
	});
}

function loadArticles(loadactives = false) {
	var newslist = '';
	var tags;
	var datecolor;
	var counter = 0;
	var showByActive;
	for (var i = 0; i < _articles.length; i++) {
		if (new Date() < new Date(_articles[i].activeFrom) || (new Date() > new Date(_articles[i].activeUntil).setHours(23,59,59,999) && _articles[i].activeUntil !== null)) {// SetHours of end of day
			showByActive = ($("#actives").val() === 'false' || $("#actives").val() === 'all') ?true :false;
			datecolor = "style='background-color:#ffc7c7'";
		} else {
			showByActive = ($("#actives").val() === 'true' || $("#actives").val() === 'all') ?true :false;
			datecolor = '';
		}
		if (search(i) && /*($('#keywords').text() === 'keine' || searchTags(i)) && ($('#companies').text() === 'alle' || searchCompany(i)) &&*/ showByActive) {
			tags = '';
			for (var tag = 0; tag < _articles[i].tags.length; tag++)
				tags += _articles[i].tags[tag].tag + ((tag < _articles[i].tags.length-1) ?', ' :'');
			newslist += "<tr " + datecolor + ">" +
					"<td>" + ++counter + "</td>" +
					"<td>" + ((_articles[i].images.length > 0) ?((_articles[i].images[0].mimetype.indexOf('video') !== -1) ?'<video src="https://backend.homeinfo.de/hinews/image/' + _articles[i].images[0].id + '" style="max-width:160px; max-height:80px" preload="metadata" controls muted>Video<br/></video>' :"<img src='https://backend.homeinfo.de/hinews/image/" + _articles[i].images[0].id + "' style='max-width:160px; max-height:80px'>") :"") + "</td>" +
					"<td>" + _articles[i].title + "</td>" +
					"<td>" + (($("<p/>").html(_articles[i].text).text().length > 350) ?$("<p/>").html(_articles[i].text).text().substring(0, 350)+'...' :$("<p/>").html(_articles[i].text).text()) + "</td>" +
					"<td><span data-toggle='tooltip' title='" + tags + "'>" + ((tags.length > 20) ?tags.substring(0, 20) + '...?' :tags) + "</span></td>" +
					"<td>" + _articles[i].created.split('T').join(' ').substring(0, 16) + "</td>" +
					"<td><input type='text' class='form-control datetime active_from' data-jsonid='" + _articles[i].id + "' placeholder='" + (_articles[i].activeFrom != null ?_articles[i].activeFrom :'')+ "'></td>" +
					"<td><input type='text' class='form-control datetime active_until' data-jsonid='" + _articles[i].id + "' placeholder='" + (_articles[i].activeUntil != null ?_articles[i].activeUntil :'') + "'></td>" +
					"<td style='vertical-align: middle'>" +
						"<i class='fa fa-edit btn_edit_news pointer' style='font-size:20px; color:#a2a2a2; padding-right:10px' title='News bearbeiten' data-jsonid='" + _articles[i].id + "'></i>" +
						"<i class='fa fa-trash-o btn_delete pointer' style='font-size:20px; color:#a2a2a2;' title='News löschen'></i>" +
						"<br><font class='confirm' style='font-size:10px; display:none;'>Sicher?<BR> <a href='#' class='btn_delete_news' data-jsonid='" + i + "'>ja</a> / <a href='#' class='btn_delete'>nein</a></font>"
					"</td>" +
				"</tr>"
		}
	}
	$('#newslist').html(newslist);
	$(".datetime").datepicker({
		constrainInput: true,
        monthNames: ['Januar','Februar','März','April','Mai','Juni',
        'Juli','August','September','Oktober','November','Dezember'],
        monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun',
        'Jul','Aug','Sep','Okt','Nov','Dez'],
        dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
        dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
        dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dateFormat : "yy-mm-dd",
		onSelect: function(dateText) {
            var id = $(this).attr('data-jsonid');
            var patch = {}

            if ($(this).hasClass('active_from')) {
                patch['activeFrom'] = dateText;
            } else if ($(this).hasClass('active_until')) {
                patch['activeUntil'] = dateText;
            }

            $.ajax({
			    url: "https://backend.homeinfo.de/hinews/article/" + id,
			    type: "PATCH",
				data: JSON.stringify(patch),
				contentType: 'application/json'
			});
		}
	}, $.datepicker.regional['de']);

	/*
	if (loadactives) {
		var previousSelection = $("#actives").val();
		var activesHTML = '<option value="true">Aktive (' + (_articles.length-isNotOnDate) + ')</option>';
		$('#actives').html(activesHTML);
		$('#actives option[value="' + previousSelection + '"]').attr('selected', 'selected')
	}
	*/
	setButtons();
	$('[data-toggle="tooltip"]').tooltip({html:true});
}
function setButtons() {
	$('.btn_removekeyword').unbind();
	$('.pagechanger').click(function(e) {
		$("#pageloader").show();
		_selectedPage = $(this).data('page');
		getArticleList();
		e.preventDefault();
	});
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
			url: "https://backend.homeinfo.de/hinews/article/" + id,
			type: "DELETE",
			success: function (msg) {
				//console.log(msg);
				$("#message").html('<font size="4" color="#FF0000">Die News "' + ((title === '') ?"ohne Titel" :title) + '" wurde gelöscht.</font>');
				getPages();
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
	selection = '';
	for (company in _companies) {
		allowSelection = true;
		for (selectedKeyword = 0; selectedKeyword < $('#companies').find('span').length; selectedKeyword++) {
			if ($('#companies').find('span').eq(selectedKeyword).text() === _companies[company].id.split('&amp;').join('&') + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'')) {
				allowSelection = false;
				break;
			}
		}
		if (allowSelection)
			selection += '<option data-cid="' + _companies[company].cid + '">' + _companies[company].id + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'');
		$('#company').html(selection);
	}
	if ($('#companies').text() === '')
		$('#companies').html('alle');
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
function searchCompany(nr) {
	for (var selectedCompany = 0; selectedCompany < $('#companies').find('span').length; selectedCompany++) {
		for (var i = 0; i < _articles[nr].customers.length; i++) {
			if ($('#companies').find('span').eq(selectedCompany).data('cid') === _articles[nr].customers[i].customer)
				return true;
		}
	}
	return false;
}
