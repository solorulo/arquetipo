// JavaScript Document

$(document).ready(function(){
						   
 $(window).resize(function(){

  $('.wrapper,.wrapper_big').css({
   position:'absolute',
   left: ($(window).width() 
     - $('.wrapper, .wrapper_big').outerWidth())/2,
   top: ($(window).height() 
     - $('.wrapper, .wrapper_big').outerHeight())/2
  });
		
 });
 
 // To initially run the function:
 $(window).resize();

});