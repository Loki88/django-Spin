var CreateSpin =
{
	init: function()
	{
		var form = $('#spin-form');
		form.prop('_readyToSend', true)
		form.prepend('<div class="alert alert-block alert-error fade in">');
		var help = form.children('.alert-block').first();
		help.hide(0);
		form.prop('__all__errors', help);
		form.submit(CreateSpin.createSpin)
	},

	createSpin: function(event)
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
					$(alertBox).children('.alert').text('Spin successfully submitted');
					$(alertBox).children('.alert').alert();
					setTimeout(function(){
						$(alertBox).alert('close');
						window.location.reload();
					}, 5000);
			}
		});
	},
};


$(document).ready(CreateSpin.init);