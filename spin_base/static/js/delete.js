var deleteLink =
{
	init: function()
	{
		var csrf = $('input[name="csrfmiddlewaretoken"]').first()
		var deleteThis = $('.delete-this');
		for(i=0; i<deleteThis.length; i++)
		{
			$(deleteThis[i]).prop('_csrf', csrf.val());
			$(deleteThis[i]).click(deleteLink.deleteThis);
		}
	},

	deleteThis: function(event)
	{
		event.preventDefault();
		if(confirm('Are you sure to delete this '+$(this).data('name')+'?'))
		{
			$.post($(this).prop('href'), {'csrfmiddlewaretoken': $(this).prop('_csrf')}).done(function()
				{
					window.location.reload();
				});
		}
	},
};

$(document).ready(deleteLink.init);