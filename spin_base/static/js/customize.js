var MakeChangesAffectTemplate=
{
	init: function()
	{
		var form = $('#customize-form');
		var picker = $('#picker');
		var wellInput = form.find('#well');
		wellInput.prop('_target', $('.well'));
		wellInput.prop('_changer', picker);
		wellInput.focusin(MakeChangesAffectTemplate.backgroundColorChange);
		var navInput = form.find('input:checkbox');
		navInput.prop('_target', $('.navbar'));
		navInput.change(MakeChangesAffectTemplate.invertNavbar);
		var backgroundColorInput = form.find('#bkgr');
		backgroundColorInput.prop('_target', $('body'));
		backgroundColorInput.prop('_changer', picker);
		backgroundColorInput.focusin(MakeChangesAffectTemplate.backgroundColorChange);
		var backgroundImageInput = form.find('select');
		backgroundImageInput.prop('_target', $(document).find('body'));
		$(backgroundImageInput).change(MakeChangesAffectTemplate.backgroundImageChange);
	},

	backgroundColorChange: function(event)
	{
		var picker = $(this).prop('_changer');
		$(picker).prop('_input', $(this));
		$(picker).mousemove(MakeChangesAffectTemplate.changeColor);
		$(this).focusout(function(event){
			var picker = $(this).prop('_changer');
			$(this).prop('_target').css('background-color', $(this).val());
			$(picker).off('mousemove', MakeChangesAffectTemplate.changeColor);
		})
	},

	changeColor: function(event)
	{
		var target = $(this).prop('_input').prop('_target');
		target.css('background-color', $(this).prop('_input').val());
	},

	invertNavbar: function(event)
	{
		target = $(this).prop('_target');
		$(target).toggleClass('navbar-inverse');
	},

	backgroundImageChange: function(event)
	{
		target = $(this).prop('_target');
		var option = $(this).find(':selected');
		var url = '/spin-media/img/custom_background/';
		url += option.text();
		url = 'url("'+url+'")';
		target.css('background-image', url);
		target.css('background-repeat', 'no-repeat');
		target.css('-moz-background-size', 'cover');
		target.css('-webkit-background-size', 'cover');
		target.css('-o-background-size', 'cover');
		target.css('background-size', 'cover');
	},
};

$(document).ready(MakeChangesAffectTemplate.init);