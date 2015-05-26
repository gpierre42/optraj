jQuery("document").ready(function($){
	
	var nav = $('#floating-menu');
	var decal = 50
	
	$('#floating-menu').css("position","absolute");
	$('#floating-menu').css("top",decal+"px");

	$(window).scroll(function () {
		if ($(this).scrollTop() > decal) {
			$('#floating-menu').css("position","fixed");
			$('#floating-menu').css("top","0px");
		} else {
			$('#floating-menu').css("position","relative");
			$('#floating-menu').css("top","auto");
		}

	});

});