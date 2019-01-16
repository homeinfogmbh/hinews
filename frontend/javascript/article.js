var _keywords; // JSON from backend
var _companies; // JSON from backend
var _id; // ID of object from GET
var _upload;
var _article = null;
$(document).ready(function() {
	_id = getURLParameterByName('id');
	_upload = new Upload($('#upload'));
	if (_id !== null)
		$('#headline').html("<i class='fa fa-edit'></i> News bearbeiten");
	// Get keywords
	$.ajax({
		url: 'https://backend.homeinfo.de/hinews/tags',
		type: 'GET',
		success: function (tags) {
			_keywords = tags;
			_keywords.sort(function(a, b) {
				return compareStrings(a, b);
			});
			// Get customers
			$.ajax({
				url: 'https://backend.homeinfo.de/hinews/customers',
				type: 'GET',
				success: function (customers) {
					//console.log(customers);
					_companies = customers;
					_companies.sort(function(a, b) {
						return compareStrings(a.id, b.id);
					})
					if (_id === null) {
						$('#keywords').html('keine');
						$('#companies').html('alle');
						setKeywordSelections();
						$('#pageloader').hide();
					} else
						getArticle();
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
	
	$(".datetime").datepicker({
		constrainInput: true,
        monthNames: ['Januar','Februar','März','April','Mai','Juni',
        'Juli','August','September','Oktober','November','Dezember'],
        monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun',
        'Jul','Aug','Sep','Okt','Nov','Dez'],
        dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
        dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
        dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dateFormat : "yy-mm-dd"
	}, $.datepicker.regional['de']);
	$('#newstext').ckeditor();
	
	//for (var i in CKEDITOR.instances) {
		//CKEDITOR.instances['newstext'].on('change', function(e) {
			//$('#newstextcount').html('Zeichen: <font color="' + (($('#newstext').val().length < 350) ?'green' :'red') + '" style="font-size:16px">' + $('#newstext').val().length + '</font>');
		//});
		CKEDITOR.instances['newstext'].on('key', function (e) { 
			$('#newstextcount').html('Zeichen: <font color="' + (($('#newstext').val().length+1 < 350) ?'green' :'red') + '" style="font-size:16px">' + ($('#newstext').val().length+1) + '</font>');
			if (e.data.keyCode == 13 || e.data.keyCode == 32)
				holdSession();
		});
	//}
	
	$('.keywords').click(function(e) {
		holdSession();
		if ($(this).val() !== null) {
			var selector;
			if ($(this)[0].id === 'company')
				selector = $('#companies');
			else
				selector = $('#keywords');
			
			if (selector.text() === 'keine' || selector.text() === 'alle')
				selector.empty();
			selector.append("<div class='btn_removekeyword pointer'><span class='label label-default' style='margin-right:5px; display: inline-block'>" + $(this).val() + "<i class='fa fa-times' style='margin-left:5px'></i></span><br></div>");
			setButtons();
			$('option:selected', this).remove();
		}
	});
	
	$('.btn_save').click(function(e) {
		$(this).attr("disabled", "disabled");
		$('#pageloader').show();
		holdSession();
		if ($(this).text().indexOf('anlegen') !== -1) {
			window.location.href = "article.html";
		} else {
			var article = {'tags':[], 'customers':[]}; // If no key given, it will not change in database
			//if ($('#keywords').find('span').length > 0)
				//article.tags = [];
			for (var selectedKeyword = 0; selectedKeyword < $('#keywords').find('span').length; selectedKeyword++)
				article.tags.push($('#keywords').find('span').eq(selectedKeyword).text());
			//if ($('#companies').find('span').length > 0)
				//article.customers = [];
			for (var selectedCompany = 0; selectedCompany < $('#companies').find('span').length; selectedCompany++) {
				for (company in _companies) {
					if ($('#companies').find('span').eq(selectedCompany).text() === _companies[company].id.toString().split('&amp;').join('&') + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'')) {
						article.customers.push(_companies[company].id);
						break;
					}
				}
			}
			article.title = $("#title").val();
			if ($("#subtitle").val() != '')
				article.subtitle = $("#subtitle").val();
			//if ($("#newstext").val() != '')
				article.text = $("#newstext").val();
			//if ($("#source").val() != '')
				article.source = $("#source").val();
			if ($("#active_from").val() != '')
				article.activeFrom = $("#active_from").val();
			if ($("#active_until").val() != '')
				article.activeUntil = $("#active_until").val();
			//console.log(article);

			var url = "https://backend.homeinfo.de/hinews/article";
			var type = 'POST';
			if (_id !== null) {
				url = "https://backend.homeinfo.de/hinews/article/" + _id;
				type = 'PATCH';
			}
			$.ajax({
				url: url,
				type: type,
				data: JSON.stringify(article),
				contentType: 'application/json',
				success: function (msg) {
					//console.log(msg);
					setImageSources();
					if (msg.id !== undefined) // For new articles
						_id = msg.id;
					_upload.uploadFile("https://backend.homeinfo.de/hinews/article/" + _id + "/images");
				},
				error: function (msg) {
					uploadCompleted(msg);
				}
			});
		}
	});
});

function getArticle() {
	$.ajax({
		url: "https://backend.homeinfo.de/hinews/article/" + _id,
		type: "GET",
		success: function (article) {
			_article = article;
			$('#headline').html("<i class='fa fa-edit'></i> News bearbeiten <font style='font-size:14px'>von Benutzer <b>" + article.author.id + "</b> vom <b>" + article.created.split('T').join(' ') + '</b>.' + ((article.editors.length > 0) ?'<br> Letze Änderung am <b>' + article.editors[article.editors.length-1].timestamp.split('T').join(' ') + '</b> von Benutzer <b>' + article.editors[article.editors.length-1].account.id + '</b>' :'') + '</font>');
			$("#title").val($("<p/>").html(article.title).text());
			$("#subtitle").val($("<p/>").html(article.subtitle).text());
			if (article.text !== '')
				$("#newstext").val(jQuery.parseHTML(article.text)[0].data);
			$("#source").val(article.source);
			for (var articel_image = 0; articel_image < article.images.length; articel_image++)
				_upload.loadImage('https://backend.homeinfo.de/hinews/image/' + article.images[articel_image].id, article.images[articel_image].source, article.images[articel_image].id, article.images[articel_image].mimetype);
			
			if (article.tags.length > 0) {
				for (var selectedKeyword = 0; selectedKeyword < article.tags.length; selectedKeyword++)
					$('#keywords').append("<div class='btn_removekeyword pointer'><span class='label label-default' style='margin-right:5px; display: inline-block'>" + article.tags[selectedKeyword].tag + "<i class='fa fa-times' style='margin-left:5px'></i></span><br></div>");
			} else
				$('#keywords').html('keine');
			if (article.customers.length > 0) {
				for (var selectedCompany = 0; selectedCompany < article.customers.length; selectedCompany++) {
					for (company in _companies) {
						if (article.customers[selectedCompany].id == _companies[company].id) {
							$('#companies').append("<div class='btn_removekeyword pointer'><span class='label label-default' style='margin-right:5px; display: inline-block'>" + _companies[company].id.toString().split('&amp;').join('&') + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'') + "<i class='fa fa-times' style='margin-left:5px'></i></span><br></div>");
							break;
						}
					}
				}
			} else
				$('#companies').html('alle');
			setButtons();
			setKeywordSelections();
			$("#active_from").val(article.activeFrom )
			$("#active_until").val(article.activeUntil);
			$('#pageloader').hide();
		},
		error: function (msg) {
			//JSON.stringify(msg);
			console.log(msg);
			$('#message').html('<font color="red"><b>FEHLER (article):</b></font> ' + msg.responseText);
		}
	});
}

function setButtons() {
	$('.btn_removekeyword').unbind();
	$('.btn_removekeyword').click(function(e) {
		holdSession();
		$(this).remove();
		setKeywordSelections();
	});
}

function setKeywordSelections() {
	var selection = '';
	var allowSelection;
	var selectedKeyword;
	for (keyword in _keywords) {
		allowSelection = true;
		for (selectedKeyword = 0; selectedKeyword < $('#keywords').find('span').length; selectedKeyword++) {
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
			if ($('#companies').find('span').eq(selectedKeyword).text() === _companies[company].id.toString().split('&amp;').join('&') + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'')) {
				allowSelection = false;
				break;
			}
		}
		if (allowSelection)
			selection += '<option>' + _companies[company].id + ((_companies[company].hasOwnProperty('annotation')) ?' (' + _companies[company].annotation + ')' :'');
		$('#company').html(selection);
	}
	if ($('#companies').text() === '')
		$('#companies').html('alle');
}

function setImageSources() {
	if (_article !== null) {
		for (var article = 0; article < _article.images.length; article++) {
			if ($('.img_source').length > 0 && $('.img_source').eq(article).val() !== _article.images[article].source) {
				var data =  {'source': $('.img_source').eq(article).val()};
				$.ajax({
					url: 'https://backend.homeinfo.de/hinews/image/' + _article.images[article].id,
					type: 'PATCH',
					data: JSON.stringify(data),
					contentType: 'application/json',
					success: function (msg) {
						//console.log(msg);
					},
					error: function (msg) {
						console.log(msg);
					}
				});
			}
		}
	}
}

function deleteImageFromArticle(id) {
	for (var article in _article.images) {
		if (_article.images[article].id == id) {
			_article.images.splice(article, 1);
			break;
		}
	}
}

function uploadCompleted(msg = 'success') {
	if (msg === 'success') {
		msg = '<font color="green"><b>Die News wurde erfolgreich gespeichert.</b></font>';
		$('.btn_save').html("<i class='fa fa-cubes'></i> Neue News anlegen");
	} else {
		msg = '<font color="red"><b>FEHLER:</b></font> ' + msg.responseText;
		
	}
	$('#message').html(msg);
	$('.btn_save').removeAttr("disabled");
	$('#pageloader').hide();
}
