var CommentForm =
{
	init: function()
	{
		var formArea = $('.comment-area');
		for( i=0; i<formArea.length; i++)
		{
			var area = $(formArea[i]);
			area.find('textarea').after('<span id="spin-count" data-length="140" class="input-mini uneditable-input"></span>');
			area.slideUp(0);
			var button = CommentForm.prepareField(area);
			button.click(CommentForm.toggleSlide);
			var form = area.find('form');
			form.prepend('<div class="alert alert-block alert-error fade in">');
			var help = form.children('.alert-block').first();
			help.hide(0);
			form.prop('__all__errors', help);
			form.submit(CommentForm.submitComment);
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

	submitComment: function(event)
	{
		event.preventDefault();
		var form = $(this);
		var url_to = form.prop('action');
		var data_form = new FormData(this);
		$.ajax({
			async: true,
			data: data_form,
			url: url_to,
			processData: false,
  			contentType: false,
			type: 'POST',
			error: function(jqXHR, status, error){
				var form_errors = jqXHR['responseJSON'];
				if(form_errors['__all__'] != undefined)
				{
					form.prop('__all__errors').html(form_errors['__all__']);
					form.prop('__all__errors').show(400);
				}
			},
			success: function(data, status, jqXHR){
					$('#body').prepend('<div class="row-fluid" id="alert-success"><div class="alert alert-success fade in"></div></div>');
					var alertBox = $('#body').find('#alert-success');
					$(alertBox).children('.alert').text('Comment successfully submitted');
					$(alertBox).children('.alert').alert();
					setTimeout(function(){
						$(alertBox).alert('close');
						window.location.reload();
					}, 5000);
			}
		});
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
			var form = EditSpin.prepareButton(button, csrf);
			button.click(EditSpin.toggleForm);
			form.prepend('<div class="alert alert-block alert-error fade in">');
			var help = form.children('.alert-block').first();
			help.hide(0);
			form.prop('__all__errors', help);
			form.submit(EditSpin.updateSpin);
		}
	},

	prepareButton: function(button, csrf)
	{
		button.prop('_actionForm', button.data('to'));
		var content = button.parentsUntil('.spin-box').parent().find('.spin-content');
		content.before('<form method="post" class="update-spin">');
		var form = content.prev('form');
		form.fadeOut(0);
		button.prop('_form', form);
		form.attr('action', button.data('to'))
		form.append($(csrf).clone())
		form.append('<textarea class="spin-area row-fluid" style="resize:none" name="content">');
		var textarea = form.find('textarea');
		button.prop('_textArea', textarea);
		textarea.val(content.text());
		button.prop('_place', content);
		textarea.after('<span id="spin-count" data-length="140" class="input-mini uneditable-input"></span>');
		form.append('<div class="row-fluid"><input class="btn" type="submit" /></div>');
		return form;
	},

	toggleForm: function(event)
	{
		event.preventDefault();
		$(this).prop('_place').fadeToggle(0);
		$(this).prop('_form').fadeToggle(0);
	},

	updateSpin: function(event)
	{
		event.preventDefault();
		var form = $(this);
		var url_to = form.prop('action');
		var data_form = new FormData(this);
		$.ajax({
			async: true,
			data: data_form,
			url: url_to,
			processData: false,
  			contentType: false,
			type: 'POST',
			error: function(jqXHR, status, error){
				var form_errors = jqXHR['responseJSON'];
				if(form_errors['__all__'] != undefined)
				{
					form.prop('__all__errors').html(form_errors['__all__']);
					form.prop('__all__errors').show(400);
				}
				var modal = form.parent('.modal');
				modal.modal('show');
			},
			success: function(data, status, jqXHR){
					var modal = form.parent('.modal');
					modal.modal('hide');
					$('#body').prepend('<div class="row-fluid" id="alert-success"><div class="alert alert-success fade in"></div></div>');
					var alertBox = $('#body').find('#alert-success');
					console.log(alertBox);
					$(alertBox).children('.alert').text('Spin updated successfully');
					$(alertBox).children('.alert').alert();
					setTimeout(function(){
						$(alertBox).alert('close');
						window.location.reload();
					}, 5000);
			}
		});
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
		var button = $(list).prev('.comment-toggle').children('.display-comment-button');
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