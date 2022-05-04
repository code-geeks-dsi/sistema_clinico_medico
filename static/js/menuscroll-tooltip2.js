// navbar animation
$(window).scroll(function() {
			if ($("#menu").offset().top > 56) {
				$("#menu").addClass("bg-primary");
			} else {
				$("#menu").removeClass("bg-primary");
			}
		});
//habilitacion de tooltips
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
  });
function irArriba(pixeles) {
	// body...
	window.addEventListener("scroll", () => {
		var scroll = document.documentElement.scrollTop;
		//console.log(scroll);

		if(scroll > pixeles){
			btnSubir.style.right = 20 + "px";
		}
		else{
			btnSubir.style.right = -100 + "px";
		}
	})
}
irArriba(300);

	
