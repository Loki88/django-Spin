var Carousel =
{
	carousel: undefined,
	current: undefined,

	init: function()
	{
		Carousel.prepareCarousel();
		var carouselLink = $('.carousel-image');
		for(i=0; i<carouselLink.length; i++)
		{
			var link = $(carouselLink[i]);
			link.click(Carousel.carouselChange);
		}
	},

	prepareCarousel: function()
	{
		Carousel.carousel = $('#image-carousel');
		Carousel.carousel.detach();
		$('body').prepend(Carousel.carousel);
		Carousel.carousel.hide(0);
		Carousel.carousel.append('<div class="carousel-inner">');
		Carousel.items = Carousel.carousel.find('.carousel-inner');
		//Carousel.getImagesLink();
		Carousel.carousel.find('.left').click(function(event){
			event.preventDefault();
			Carousel.carousel.carousel('prev');
		});
		Carousel.carousel.find('.right').click(function(event){
			event.preventDefault();
			Carousel.carousel.carousel('next');
		});;
	},

	getImagesLink: function()
	{
		var links = $('#images-links').data('links');
		if(links != undefined )
			eval( "Carousel.images = "+links);
	},

	carouselChange: function(event)
	{
		event.preventDefault();
		var number = parseInt($(this).data('nr'));
		Carousel.getImages();
		Carousel.carousel.carousel(number-1);
		Carousel.carousel.modal('show');
		Carousel.current = number-1;
	},

	getImages: function()
	{
		var containers = Carousel.carousel.find('.item');
		for(i=0; i<containers.length; i++)
		{
			var container = $(containers[i]);
			if(container.children('img').length == 0)
			{
				container.append('<img class="img-polaroid" >');
				var img = container.children('img');
				img.prop('src', container.data('src'));
			}
		}
	}
	
};

$(document).ready(Carousel.init)