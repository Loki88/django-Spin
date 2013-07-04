
// var StartPicker =
// {
// 	init: function()
// 	{
// 		var colorInput = $('.colorInput');
// 		for(i=0; i<colorInput.length; i++)
// 		{
// 			var input = $(colorInput[i]);
// 			var picker = $(input).next('#colorpicker'+input.id);
// 			picker.farbtastic(input);
// 		}
// 	}
// }

// $(document).ready(StartPicker.init)

$(document).ready(function() {
    var f = $.farbtastic('#picker');
    var p = $('#picker').css('opacity', 0.25);
    var selected;
    $('.colorInput')
      .each(function () { f.linkTo(this); $(this).css('opacity', 0.75); })
      .focus(function() {
        if (selected) {
          $(selected).css('opacity', 0.75).removeClass('colorwell-selected');
        }
        f.linkTo(this);
        p.css('opacity', 1);
        $(selected = this).css('opacity', 1).addClass('colorwell-selected');
      });
  });