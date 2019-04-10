	$(function(){
			$(".nav>li").mouseenter(function(){
					$(this).addClass("currents");
				$(this).siblings().removeClass("currents");
				});
	});     