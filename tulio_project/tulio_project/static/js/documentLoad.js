$(document).ready(function() {
	getComments()
	//========================
	//Screens
	//========================

	$('a.login-window').click(function() {
		
                //Getting the variable's value from a link 
		var loginBox = $(this).attr('href');

		//Fade in the Popup
		$(loginBox).fadeIn(300);
		
		//Set the center alignment padding + border see css style
		var popMargTop = ($(loginBox).height() + 24) / 2; 
		var popMargLeft = ($(loginBox).width() + 24) / 2; 
		
		$(loginBox).css({ 
			'margin-top' : -popMargTop,
			'margin-left' : -popMargLeft
		});
		
		// Add the mask to body
		$('body').append('<div id="mask"></div>');
		$('#mask').fadeIn(300);
		
		return false;
	});

	$('a.upload-window').click(function() {
		
                //Getting the variable's value from a link 
		var uploadBox = $(this).attr('href');

		//Fade in the Popup
		$(uploadBox).fadeIn(300);
		
		//Set the center alignment padding + border see css style
		var popMargTop = ($(uploadBox).height() + 24) / 2; 
		var popMargLeft = ($(uploadBox).width() + 24) / 2; 
		
		$(uploadBox).css({ 
			'margin-top' : -popMargTop,
			'margin-left' : -popMargLeft
		});
		
		// Add the mask to body
		$('body').append('<div id="mask"></div>');
		$('#mask').fadeIn(300);
		
		return false;
	});

	$('a.contact-window').click(function() {
		
                //Getting the variable's value from a link 
		var contactBox = $(this).attr('href');

		//Fade in the Popup
		$(contactBox).fadeIn(300);
		
		//Set the center alignment padding + border see css style
		var popMargTop = ($(contactBox).height() + 24) / 2; 
		var popMargLeft = ($(contactBox).width() + 24) / 2; 
		
		$(contactBox).css({ 
			'margin-top' : -popMargTop,
			'margin-left' : -popMargLeft
		});
		
		// Add the mask to body
		$('body').append('<div id="mask"></div>');
		$('#mask').fadeIn(300);
		
		return false;
	});
	
	// When clicking on the button close or the mask layer the popup closed
	$('a.close, #mask').live('click', function() { 
	  $('#mask , .login-popup').fadeOut(300 , function() {
		$('#mask').remove();  
		}); 
	  $('#mask , .upload-popup').fadeOut(300 , function() {
		$('#mask').remove();  
		}); 
	  $('#mask , .contact-popup').fadeOut(300 , function() {
		$('#mask').remove();  
		});
	return false;
	});
});