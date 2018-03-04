$(document).ready(function(){
	var blogshowcounter = 0; // to keep track of current slide
	$blogshowitems = $('.homeslideshow figure'); // a collection of all of the slides, caching for performance
	blognumItems = $blogshowitems.length; //total number of slides
	$blogshowitems.eq(0).addClass('show'); //show first item as soon as page loads.

	/*** this function cycles through slides. showing the next or prev slide and hiding all others ***/
	var blogshowCurrent = function(){
		// calculates the actual index of the element to show
		var blogitemToShow = Math.abs(blogshowcounter%blognumItems);
		// remove .show from whichever element currently has it.
		$blogshowitems.removeClass('show');
		//add .show only to the current slide
		$blogshowitems.eq(blogitemToShow).addClass('show');
	};


	// add click events to prev and next buttions

	$('.next').on('click', function(){
		blogshowcounter++;
		blogshowCurrent();
	});
	$('.prev').on('click', function(){
		blogshowcounter--;
		blogshowCurrent();
	});

	// add swipe feature for touch devices
	if('ontouchstart' in window){
		$(".diy-slideshow").swipe({
			swipeLeft:function() {
				blogshowcounter++;
				blogshowCurrent();
			},
			swipeRight:function() {
				blogshowcounter--;
				blogshowCurrent();
			}
		});
	}

	$('.slideshowlink').on('click', function(){
		openNav();
		blogTitle = this.parentNode.textContent;
		jsonobj = '{"blogtitle":"' + blogTitle  + '"}'
		 $.ajax({
                method: "POST",
                dataType: "json",
                url: "/blogview/",
                contentType: "application/json",
                async: true,
                processData: false,
                data: jsonobj,
                context: document.body,
                beforeSend: function(){
                	$('.overlay').show();
                } ,
                statusCode: {
                    404: function () {
                    	// End 404 func
                    },
                    401: function () {
                    }, // End 401 func
                    200: function (data, status, XHR) {
						var thishtml = data['htmlresponse']
                    	 $('#overlay-content').append(thishtml);
                    } //End 200 func
                } // End statusCode
            }).fail(function(){
            });
	});

	$('.signup').on('click', function(){
		openNav();
		 $.ajax({
                method: "POST",
                dataType: "json",
                url: "/members/signup",
                contentType: "application/json",
                async: true,
                processData: false,
                context: document.body,
                beforeSend: function(){
                	$('.overlay').show();
                } ,
                statusCode: {
                    404: function () {
                    	// End 404 func
                    },
                    401: function () {
                    }, // End 401 func
                    200: function (data, status, XHR) {
						var thishtml = data['htmlresponse']
                    	 $('#overlay-content').append(thishtml);
                    } //End 200 func
                } // End statusCode
            }).fail(function(){
            });
	});
});

/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("myNav").style.width = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}