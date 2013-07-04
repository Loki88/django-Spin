var FormUpload =
{
	init: function()
	{
		var forms = $('.spin-form-upload');
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
					FormUpload.prepareFields(input);
					if(input.prop('type') == 'file')
					{
						var files = form.prop('_files');
						if(files != undefined)
							files[files.length] = input;
						else
							files = [input, ]
						form.prop('_files', files);
						input.change(FormUpload.fileChange);
					}
				}
				form.submit(FormUpload.validateField);
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
		var url_to = $(this).prop('action');
		var data_form = new FormData(this);
		var form = $(this)
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
					var all = form_errors['__all__'];
					console.log(all);
					console.log(form.prop('__all__errors'))
					form.prop('__all__errors').text(all);
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
							if(error_box.html().length > 0)
								error_box.html(error_box.html()+'<br/>'+field_errors[k])
							else
								error_box.text(field_errors[k])
						}
						error_box.show(400);
					}
				}
			},
			success: function(data, status, jqXHR){
				$(window.location).attr('href', data['redirect']);
			}
		})
		// try
		// {
		// 	var xhr = new XMLHttpRequest();
		// }
		// catch(error)
		// {
		// 	try
		// 	{
		// 		var xhr = new ActiveXObject("Microsoft.XMLHTTP");
		// 	}
		// 	catch(error)
		// 	{
		// 		var xhr = null
		// 	}
		// }
		// if(xhr == null)
		// {
		// 	$(this).submit();
		// }
		// else
		// {
		// 	xhr.upload.addEventListener('progress',function(ev){
		// 	    console.log((ev.loaded/ev.total)+'%');
		// 	}, false);
		// 	xhr.onreadystatechange = function(event){
		// 	    if(this.readystate == 4)
		// 	    {
		// 	    	if(this.status == 200 || this.status == 304)
		// 	    }
		// 	};
		// 	xhr.open('POST', url, true);
		// 	var files = document.getElementById('file-input-element').files;
		// 	var data = new FormData();
		// 	for(var i = 0; i < files.length; i++) data.append('file'+i, files[i]);
		// 	xhr.send(data);
		// }
	},

	fileChange: function(event)
	{
		event.preventDefault();
		console.log($(this));
		files = $(this).prop('files');
		for(i=0; i<files.length; i++)
		{
			console.log($(files[i]))
		}
	}
};

$(document).ready(FormUpload.init);