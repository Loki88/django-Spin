var SpinForm =
{
	init: function()
	{
		var spinArea = $('.spin-area');
		for(i=0; i<spinArea.length; i++)
		{
			var spin = $(spinArea[i]);
			SpinForm.prepareToSpin(spin);
			spin.focusin(SpinForm.focusHandler);
			spin.focusout(SpinForm.stopTyping);
		}
	},

	prepareToSpin: function(textArea)
	{
		var text = textArea.val();
		textArea.prop('_textValue', text);
		var counter = $(textArea).next('#spin-count');
		textArea.prop('_textCounter', counter)
		var maxLength = counter.data('length')
		counter.prop('_textMaxLength', maxLength);
		if(text.length > maxLength)
		{
			text = text.slice(0, maxLength);
			textArea.val(text)
		}
		counter.prop('_textSubmitted', text);
		var length = maxLength-text.length;
		counter.prop('_textLength', length);
		counter.text(length);
	},

	focusHandler: function(event)
	{
		event.preventDefault();
		$(this).keyup(SpinForm.textCount);
		$(this).change(SpinForm.textCount);
	},

	textCount: function(event)
	{
		var text = $(this).val();
		var counter = $(this).prop('_textCounter');
		var maxLength = counter.prop('_textMaxLength');
		if(text.length > maxLength)
		{
			text = text.substr(0, maxLength);
			$(this).val(text)
		}
		counter.prop('_textSubmitted', text);
		var length = maxLength-text.length;
		counter.prop('_textLength', length);
		counter.text(length);
	},

	stopTyping: function(event)
	{
		event.preventDefault();
		$(this).unbind('keypress', SpinForm.textCount);

	}
};



$(document).ready(SpinForm.init)
