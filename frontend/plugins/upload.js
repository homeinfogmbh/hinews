//var _upload = []; // Static

class Upload {
	constructor(selector, maximages) {
		this.selector = selector;
		this.maximages = maximages;
		this.fileList = [];
		this.newImageID = 0;
		this.selector.css({'border': '2px solid #a2a2a2', 'min-height': '100px', 'width':'100%', 'padding': '5px'});
		this.selector.html("<div id='upload_error'></div>Hierher ziehen oder <input type='file' id='input' multiple style='display:none'>" +
		"<button class='btn btn-primary btn_input'><i class='fa fa-folder-open'></i> auswählen</button><br><br>" +
		'<div id="upload_thumbnail"></div>');
		
		var thisobject = this;
		this.selector.find('#input').get(0).addEventListener("change", function(evt) {
			evt.stopPropagation();
			evt.preventDefault();
			thisobject.drop(this.files);
		}, false);
		this.selector.get(0).addEventListener('dragover', function(evt) {
			evt.stopPropagation();
			evt.preventDefault();
			evt.dataTransfer.dropEffect = 'copy'; 
			try { thisobject.selector.css({'border': '2px solid red'}); } catch(err) { }
		}, false);
		this.selector.get(0).addEventListener('dragleave', function(evt) {
			evt.stopPropagation();
			evt.preventDefault();
			try { thisobject.selector.css({'border': '2px solid #a2a2a2'}); } catch(err) { }
		}, false);
		this.selector.get(0).addEventListener('drop', function(evt) {
			evt.stopPropagation();
			evt.preventDefault();
			thisobject.drop(evt.dataTransfer.files);
		}, false);
		
		// Prevent browser outside the field from loading a drag-and-dropped file
		window.addEventListener("dragenter", function(e) {
			e.preventDefault();
			e.dataTransfer.effectAllowed = "none";
			e.dataTransfer.dropEffect = "none";
		}, false);
		window.addEventListener("dragover", function(e) {
			e.preventDefault();
			e.dataTransfer.effectAllowed = "none";
			e.dataTransfer.dropEffect = "none";
		});
		window.addEventListener("drop", function(e) {
			e.preventDefault();
			e.dataTransfer.effectAllowed = "none";
			e.dataTransfer.dropEffect = "none";
		});
		$('.btn_input').unbind()
		$('.btn_input').click(function() {
			$(this).parent().find("#input").trigger("click");
		});	
	}

	drop(fileList) {
		holdSession();
		var thisobject = this;
		try { thisobject.selector.css({'border': '2px solid #a2a2a2'}); } catch(err) { }

		// Permissions
		for (var i = 0, f; f = fileList[i]; i++) {
			if (!f.type.match('image.*') && !f.type.match('video.*')) {
				thisobject.selector.find('#upload_error').html('<font style="color:red; font-size:16px">' + f.name + ' nicht erlaubt</font>');
				continue;
			} else if (f.size > 104857600) { // 100mb
				thisobject.selector.find('#upload_error').html('<font style="color:red; font-size:16px">' + f.name + ' ist zu groß (max. 5mb)</font>');
				continue;
			} else if (i >= thisobject.maximages || thisobject.fileList.length >= thisobject.maximages) {
				thisobject.selector.find('#upload_error').html('<font style="color:red; font-size:16px">' + f.name + ' ist zuviel</font>');
				continue;
			}
			// Create thumbnails
			var reader = new FileReader();
			reader.onload = (function(file) {
				return function(e) {
					if (file.type.match('video.*')) {
						thisobject.selector.find('#upload_thumbnail').append('<div class="thumb" data-id="n' + thisobject.newImageID + '">' +
							'<video src="' + e.target.result + '" height="300" style="max-width:200px; max-height:150px; border:2px solid transparent;" title="' + file.name + ' (' + (file.size/1024).toFixed(2) + 'kb)" preload="metadata" controls muted>Ihr Browser kann dieses Video nicht wiedergeben.<br/></video>' + 
							'<i class="fa fa-trash-o btn_delete_image pointer" style="font-size:20px; color:#ff0000; margin:10px 5px; vertical-align: top; display:none" title="Bild löschen"></i>' +
							'<input type="text" class="form-control" placeholder="Quelle eingeben"><br>'+
						'</div>')
					} else if (file.type.match('image.*')) {
						thisobject.selector.find('#upload_thumbnail').append('<div class="thumb" data-id="n' + thisobject.newImageID + '">' +
							'<img src="' + e.target.result + '" style="max-width:200px; max-height:150px; border:2px solid transparent;" title="' + file.name + ' (' + (file.size/1024).toFixed(2) + 'kb)">' + 
							'<i class="fa fa-trash-o btn_delete_image pointer" style="font-size:20px; color:#fff; margin:10px -30px; vertical-align: top; display:none" title="Bild löschen"></i>' +
							'<input type="text" class="form-control" placeholder="Quelle eingeben"><br>'+
						'</div>')
					}
					thisobject.fileList.push({'file': file, 'id':thisobject.newImageID});
					thisobject.newImageID++;
					thisobject.setButtons();
				};
			})(f);
			reader.readAsDataURL(f);
		}
	}

	uploadFile(url) {
		if (this.fileList.length > 0) {
			var thisobject = this;
			var data = new FormData();
			var json;
			data.append('image', this.fileList[0].file);
			for (var source = 0; source < thisobject.selector.find('#upload_thumbnail').find('.thumb').length; source++) {
				if (thisobject.selector.find('#upload_thumbnail').find('.thumb').eq(source).data('id').toString().indexOf('n') !== -1 && thisobject.selector.find('#upload_thumbnail').find('.thumb').eq(source).data('id').toString().substring(1) == this.fileList[0].id) {
					json = {"source":thisobject.selector.find('#upload_thumbnail').find('.thumb').eq(source).find('input').val()};
					break;
				}
			}
			var bytes = JSON.stringify(json).split('');
			var jsonFile;
			if ((navigator.userAgent.indexOf("Edge") > -1 || navigator.userAgent.indexOf("Trident/7.0") > -1) ?true :false)
				jsonFile = new Blob(bytes, 'meta.json'); 
			else
				jsonFile = new File(bytes, 'meta.json'); // Not supported in edge 
			data.append('metadata', jsonFile);
			$.ajax({
				url: url,
				type: "POST",
				data: data,
				cache: false,
				contentType: false,
				processData: false,
				success: function (msg) {
					thisobject.fileList.shift();
					if (thisobject.fileList.length === 0)
						uploadCompleted('success');
					else
						thisobject.uploadFile(url);
				},
				// Progress bar
				/*
				xhr: function() {
					var xhr = new window.XMLHttpRequest();
					//Upload progress
					xhr.upload.addEventListener("progress", function(evt){
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							//Do something with upload progress
							console.log(percentComplete);
						}
					}, false);
					//Download progress
					xhr.addEventListener("progress", function(evt){
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							//Do something with download progress
							console.log(percentComplete);
						}
					}, false);
					return xhr;
				},*/
				error: function (msg) {
					uploadCompleted(msg);
				}
			});
		} else {
			uploadCompleted('success');
		}
	}
	
	setButtons() {
		var thisobject = this;
		$('.thumb').unbind().mouseover();
		$('.thumb').unbind().mouseout();
		$('.btn_delete_image').unbind().click();
		$('.thumb').mouseover(function() {
			$(this).find('i').fadeIn(0);
			$(this).find('img').css({'border': '2px solid #ff0000'});
			$(this).find('video').css({'border': '2px solid #ff0000'});
		});
		$('.thumb').mouseout(function() {
			$(this).find('i').fadeOut(0);
			$(this).find('img').css({'border': '2px solid transparent'});
			$(this).find('video').css({'border': '2px solid transparent'});
		});
		$('.btn_image').click(function() {
			holdSession();
			window.open($(this).data('imageurl'), '_blank');
		});
		$('.btn_delete_image').click(function() {
			holdSession();
			var id = $(this).parent().data('id').toString();
			deleteImageFromArticle(id);
			$(this).parent().remove();
			if (id.indexOf('n') === -1) { // 'n' not uploaded yet
				$.ajax({
					url: 'https://backend.homeinfo.de/hinews/image/' + id,
					type: 'DELETE',
					success: function (msg) {
						//console.log(msg);
					},
					error: function (msg) {
						console.log(msg);
					}
				});
			} else {
				id = id.substring(1);
				for (var fileID = 0; fileID < thisobject.fileList.length; fileID++) {
					if (id == thisobject.fileList[fileID].id) {
						thisobject.fileList.splice(fileID, 1);
						break;
					}
				}
			}
		});
	}
	
	loadImage(src, sourcetext, id, mimetype) {
		if (mimetype.indexOf('video') !== -1) {
			this.selector.find('#upload_thumbnail').append('<div class="thumb" data-id="' + id + '">' +
				'<video src="' + src + '" style="max-width:200px; max-height:150px; border:2px solid transparent;" data-imageurl="' + src + '" preload="metadata" controls muted>Ihr Browser kann dieses Video nicht wiedergeben.<br/></video>' + 
				'<i class="fa fa-trash-o btn_delete_image pointer" style="font-size:20px; color:#ff0000; margin:10px 5px; vertical-align: top; display:none" title="Bild löschen"></i>' +
				'<input type="text" class="form-control img_source" placeholder="Quelle eingeben" value="' + sourcetext + '"><br>'+
			'</div>');
		} else {
			this.selector.find('#upload_thumbnail').append('<div class="thumb" data-id="' + id + '">' +
				'<img src="' + src + '" class="btn_image" style="max-width:200px; max-height:150px; border:2px solid transparent;" data-imageurl="' + src + '">' + 
				'<i class="fa fa-trash-o btn_delete_image pointer" style="font-size:20px; color:#fff; margin:10px -30px; vertical-align: top; display:none" title="Bild löschen"></i>' + 
				'<input type="text" class="form-control img_source" placeholder="Quelle eingeben" value="' + sourcetext + '"><br>'+
			'</div>')
		}
		this.setButtons();
	}
}