var Report =
{
	init: function()
	{
		var modal= $('#report-modal');
		var form = modal.find('form');
		form.prop('_modal', modal);
		Report.prepareForm(form);
		var reports = $('.report');
		for(i=0; i<reports.length; i++)
		{
			var report = $(reports[i]);
			report.prop('_form', form);
			report.click(Report.getModal)
		}
	},

	prepareForm: function(form)
	{
		$(form).prepend('<div class="alert alert-block alert-error fade in">');
		var help = $(form).children('.alert-block').first();
		help.hide(0);
		$(form).prop('__all__errors', help);
		$(form).children('.modal-footer').before('<textarea id="report-area" name="content" class="span*" style="resize: none">');
		$(form).prop('_textArea', $(form).find('textarea'));
		$(form).prop('_textArea').before('<label for="report-area">Write your report</label>');
		form.submit(Report.sendReport);
	},

	getModal: function(event)
	{
		event.preventDefault();
		var link = $(this);
		var form = link.prop('_form');
		form.prop('_textArea').val('');
		form.prop('action', link.prop('href'));
		form.prop('_modal').modal('show');
	},

	sendReport: function(event)
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
				var modal = form.prop('_modal');
				modal.modal('show');
			},
			success: function(data, status, jqXHR){
					var modal = form.prop('_modal');
					modal.modal('hide');
					$('#body').prepend('<div class="row-fluid" id="alert-success"><div class="alert alert-success fade in"></div></div>');
					var alertBox = $('#body').find('#alert-success');
					$(alertBox).children('.alert').text('Report successfully submitted');
					$(alertBox).children('.alert').alert();
					form.prop('_textArea').val('');
			}
		});
	},
};

$(document).ready(Report.init)