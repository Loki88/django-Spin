var CommentForm =
{
	init: function()
	{
		var formArea = $('.comment-area');
		for( i=0; i<formArea.length; i++)
		{
			var area = $(formArea[i]);
			area.slideUp(0);
			var button = CommentForm.prepareField(area);
			button.click(CommentForm.toggleSlide);
		}
	},

	prepareField: function(area)
	{
		var slide_button = $(area).prevUntil('.comment-spin').prev();
		slide_button.prop('_targetArea', area);
		return slide_button;
	},

	toggleSlide: function(event)
	{
		event.preventDefault();
		$(this).prop('_targetArea').slideToggle(600);
	},

};

var EditSpin =
{
	init: function()
	{
		var csrf = $('input[name="csrfmiddlewaretoken"]').first()
		var editButton = $('.edit-spin');
		for(i=0; i<editButton.length; i++)
		{
			var button = $(editButton[i]);
			EditSpin.prepareButton(button, csrf);
			button.click(EditSpin.toggleForm);
		}
	},

	prepareButton: function(button, csrf)
	{
		button.prop('_actionForm', button.data('to'));
		var content = button.parentsUntil('.spin-box').parent().find('.spin-content');
		console.log(content)
		content.before('<form method="post">');
		var form = content.prev('form');
		console.log(form)
		form.fadeOut(0);
		button.prop('_form', form);
		form.attr('action', button.data('to'))
		form.append($(csrf).clone())
		form.append('<textarea class="spin-area" name="content">')
		var textarea = form.children('textarea');
		console.log(textarea)
		button.prop('_textArea', textarea);
		textarea.val(content.text());
		button.prop('_place', content);
		textarea.after('<span id="spin-count" data-length="140" class="input-mini uneditable-input">');
		form.append('<input class="btn" type="submit" />');
	},

	toggleForm: function(event)
	{
		event.preventDefault();
		$(this).prop('_place').fadeToggle(0);
		$(this).prop('_form').fadeToggle(0);
	},

};


var CommentSlide =
{
	init: function()
	{
		var commentList = $('.comment-list');
		for( i=0; i<commentList.length; i++)
		{
			var list = $(commentList[i]);
			list.slideUp(0);
			var button = CommentSlide.setButton(list);
			button.click(CommentSlide.DisplayToggle);
		}
	},

	setButton: function(list)
	{
		var button = $(list).prevUntil('.display-comment-button').prev();
		button.prop('_commentList', list);
		return button;
	},

	DisplayToggle: function(event)
	{
		event.preventDefault();
		$(this).prop('_commentList').slideToggle(500);
	},
};

$(document).ready(CommentSlide.init)
$(document).ready(CommentForm.init)
$(document).ready(EditSpin.init)