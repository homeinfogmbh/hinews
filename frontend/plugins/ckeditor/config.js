/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';

  // Define changes to default configuration here. For example:
	config.language = 'de';
	//config.uiColor = '#F2F2F2';
  config.htmlEncodeOutput = false;
	config.entities = false;
	//config.entities_additional = '&#43;';
	config.ignoreEmptyParagraph = true;
	config.forceEnterMode = true;
	config.enterMode = CKEDITOR.ENTER_BR;
	config.shiftEnterMode = CKEDITOR.ENTER_BR;
	config.format_tags = 'p;h1;h2;h3;h4;h5;h6;address;div';

  //change <strong> to <b>
	config.coreStyles_bold = { element : 'b', overrides : 'strong' };
	config.coreStyles_italic = { element : 'i', overrides : 'em' };
	config.format_div = { element : 'div', overrides : 'p' };

  //toolbar
	config.toolbar = 'MyToolbar';
	config.toolbar_MyToolbar =
	[
		{ name: 'document', items : [ 'Source','DocProps','-', 'Cut','Copy','Paste','PasteText','PasteWord','-','Print','SpellCheck','FontSize', 'NumberedList', 'BulletedList' ] },
		{ name: 'tools', items : [ 'Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat', 'Bold','Italic','Underline', 'Table', 'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock', 'UnorderedList', 'Link','Unlink', 'FitWindow','Maximize' ] },
		{ name: 'paragraph', groups: [ 'list' ] },
		{ name: 'colors', items: [ 'TextColor' ] }
	];

	//custom styles
	config.fontSize_style =  {
    element		: 'font',
    styles		: { 'font-size' : '#(size)' },
		attributes	 : { 'size' : '#(size)' },
    overrides	: [ { element : 'font', attributes : { 'style' : null } } ]
  };

  config.colorButton_foreStyle = {
      element: 'span',
      styles: { 'color': '#(color)' },
			attributes	 : { 'color' : '#(color)' },
      overrides: [ { element: 'font', attributes: { 'style': null } } ]
  };

	//custom font sizes in the dropdown
	config.fontSize_sizes = '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;30/30px;32/32px;34/34px;36/36px;38/38px;40/40px;42/42px;44/44px;46/46px;48/48px;50/50px;52/52px;54/54px;56/56px;58/58px;60/60px;62/62px;64/64px;68/68px;70/70px;72/72px;';

};
