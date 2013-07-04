var spinForm =
{
	init: function()
	{
		var forms = $('.spin-form');
		for(i=0; i<forms.length; i++)
		{
			var form = $(forms[i]);
			if(form.prop('_readyToSend'))
			{

			}
			else
			{
				form.prop('_readyToSend', true)
				form.find('legend').after('<div class="alert alert-block alert-error fade in">');
				var help = form.find('.alert-block').first();
				help.hide(0);
				form.prop('__all__errors', help);
				var formInput = form.find('.form-input');
				form.prop('_fieldList', formInput);
				for(i=0; i<formInput.length; i++)
				{
					var input = $(formInput[i]);
					spinForm.prepareFields(input);
				}
				form.submit(spinForm.validateField);
			}
		}
	},

	prepareFields: function(input)
	{
		var groupControl = $(input).parent('.controls');
		groupControl.append('<span class="help-block">');
		var box = groupControl.children('.help-block');
		box.hide(0);
		input.prop('_errorBox', box);
	},

	validateField: function(event)
	{
		event.preventDefault();
		var data_form = $(this).serialize();
		var url_to = $(this).attr('action');
		var form = $(this);
		$.ajax({
			async: true,
			data: data_form,
			url: url_to,
			type: 'POST',
			error: function(jqXHR, status, error){
				form_errors = jqXHR['responseJSON'];
				if(form_errors != undefined)
				{
					if(form_errors['__all__'] != undefined)
					{
						form.prop('__all__errors').html(form_errors['__all__']);
						form.prop('__all__errors').show(400);
					}
					var fields = form.prop('_fieldList');
					for(i=0; i<fields.length; i++)
					{
						var field_errors = form_errors[fields[i].name]
						if(field_errors != undefined)
						{
							var control = $(fields[i]).parentsUntil('.control-group').parent('.control-group')
							control.addClass('error');
							var error_box = $(fields[i]).prop('_errorBox');
							error_box.text('');
							for(k=0; k<field_errors.length; k++)
							{
								if(error_box.html() != '')
									error_box.html(error_box.html()+'<br/>'+field_errors[k])
								else
									error_box.text(field_errors[k])
							}
							error_box.show(400);
						}
					}
				}
			},
			success: function(data, status, jqXHR){
				$(window.location).attr('href', data['redirect']);
			}

		});
		
	},
};

$(document).ready(spinForm.init)