var RegistrationForm =
{
	init: function()
	{
		var form = $('#registration-form');
		var registrationInput = $('.registration');
		form.prop('_fieldList', registrationInput);
		for(i=0; i<registrationInput.length; i++)
		{
			var input = $(registrationInput[i]);
			RegistrationForm.prepareFields(input);
		}
		form.submit(RegistrationForm.validateField());
	}

	prepareFields: function(input)
	{
		var groupControl = $(input).parent('.controls');
		groupControl.append('<span class="help-block">');
		var box = groupControl.children('.help-block');
		box.hide(0);
		input.prop('_errorBox', box);
	}

	validateField: function(event)
	{
		event.preventDefault();
		var fields = $(this).prop('_fieldList');
		var data = {}
		for(i=0; i<fields.length; i++)
		{
			data[fields.name] = fields.value;
		}
		$.post('registration/', data, function(data, status, jqXHR){
			console.log(status)
			if(status == 303)
			{
				console.log(data);
				console.log(jqXHR);
			}
			else
			{
				console.log(data);
			}
		});
		
	}
}