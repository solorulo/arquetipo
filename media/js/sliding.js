

 /* idTabs ~ Sean Catchpole - Version 2.0 - MIT/GPL */
(function(){var dep={"jQuery":"http://code.jquery.com/jquery-latest.min.js"};var init=function(){(function($){$.fn.idTabs=function(){var s={};for(var i=0;i<arguments.length;++i){var a=arguments[i];switch(a.constructor){case Object:$.extend(s,a);break;case Boolean:s.change=a;break;case Number:s.start=a;break;case Function:s.click=a;break;case String:if(a.charAt(0)=='.')s.selected=a;else if(a.charAt(0)=='!')s.event=a;else s.start=a;break;};}if(typeof s['return']=="function")s.change=s['return'];return this.each(function(){$.idTabs(this,s);});}
$.idTabs=function(tabs,options){var meta=($.metadata)?$(tabs).metadata():{};var s=$.extend({},$.idTabs.settings,meta,options);if(s.selected.charAt(0)=='.')s.selected=s.selected.substr(1);if(s.event.charAt(0)=='!')s.event=s.event.substr(1);if(s.start==null)s.start=-1;var showId=function(){if($(this).is('.'+s.selected))return s.change;var id="#"+this.href.split('#')[1];var aList=[];var idList=[];$("a",tabs).each(function(){if(this.href.match(/#/)){aList.push(this);idList.push("#"+this.href.split('#')[1]);}});if(s.click&&!s.click.apply(this,[id,idList,tabs,s]))return s.change;for(i in aList)$(aList[i]).removeClass(s.selected);for(i in idList)$(idList[i]).hide();$(this).addClass(s.selected);$(id).show();return s.change;};var list=$("a[href*='#']",tabs).unbind(s.event,showId).bind(s.event,showId);var test=false;if(typeof s.start=="number"&&(test=list.eq(s.start)).length);else if(typeof s.start=="string"&&(test=list.filter("[href*='#"+s.start+"']")).length);else if((test=list.filter(s.selected)).length);if(test)test.removeClass(s.selected.substr(1)).trigger(s.event);return s;};$.idTabs.settings={start:0,change:false,click:null,selected:".selected",event:"!click"};$.idTabs.version="2.0";$(function(){$(".idTabs").idTabs();});})(jQuery);};init();return;var check=function(o,s){s=s.split('.');while(o&&s.length)o=o[s.shift()];return o;};var head=document.getElementsByTagName("head")[0];var add=function(url){var s=document.createElement("script");s.type="text/javascript";s.src=url;head.appendChild(s);};var ok=true;for(d in dep){if(check(this,d))continue;ok=false;add(dep[d]);}if(ok)return init();var s=document.getElementsByTagName('script');add(s[s.length-1].src);})();



	$(document).ready(function(){
		$('.show').toggle(function(){
			$('#log').slideDown();
		}, function(){
			$('#log').slideUp();
		});
	});
	
	
	$(document).ready(function(){
		$('.categ').toggle(function(){
			$('#cat').slideDown();
		}, function(){
			$('#cat').slideUp();
		});
	});
	
	
	/*$(document).ready(function(){
		$('.editas').toggle(function(){
			$('#editat').slideDown();
		}, function(){
			$('#peditat').slideUp();
		});
	});
	
	
	
	$(document).ready(function(){
		$('.cpin').toggle(function(){
			$('#coloca').slideDown();
		}, function(){
			$('#coloca').slideUp();
		});
	});

*/


$(function(){
				
				$('#listapin').jqcollapse({
				   slide: true,
				   speed: 1000,
				   easing: 'easeOutCubic'
				});
				
			});
			
			
			
			
			/*$(function() {
                     var offset = $("#scrollback").offset();
                     var topPadding = 600;
                     $(window).scroll(function() {
                         if ($(window).scrollTop() > offset.top) {
                             $("#scrollback").stop().animate({
                                 marginTop: $(window).scrollTop() - offset.top + topPadding
                             });
                         } else {
                             $("#scrollback").stop().animate({
                                 marginTop: 200
                             });
                         };
                     });
                 });*/
				 
				 
				 
				 
				
				
				
	
/* 
 * Jquery Toggle Button Extension
 *
 * @author Oliver Green <green2go@gmail.com>
 * @category JQuery
 * @license Creative Commons Attribution-ShareAlike 3.0 Unported License. 
 * (http://creativecommons.org/licenses/by-sa/3.0/)
 * Date: $Date: 2011-02-27 09:24:24 +0000 (Sun, 27 Feb 2011) $
 * 
 */

jQuery.fn.toggleButton=function(c){var d=$(this).find(".toggleBtn button");if(c&&c.buttonSelector){d=$(this).find(c.buttonSelector)}var b=function(g){g.removeClass("toggled");g.parent().find("input[type=checkbox], input[type=radio]").each(function(){$(this).removeAttr("checked")})};var f=function(g){g.addClass("toggled");g.parent().find("input[type=checkbox], input[type=radio]").each(function(){$(this).attr("checked","checked")})};var a=function(){d.find("input[type=option]").each(function(){$(this).removeAttr("checked")})};var e=function(h){var g=h.parent().find("button");if(h.attr("checked")=="checked"){f(g)}else{b(g)}};$(d).each(function(){var g=$(this);g.parent().find("input[type=checkbox], input[type=radio]").each(function(){$(this).addClass("hidden");$(this).attr("tabindex","-1")});g.parent().find("label").each(function(){$(this).addClass("hidden")});g.css("display","block");g.parent().find("input[type=checkbox], input[type=radio]").each(function(){var h=$(this);e(h);$(this).change(function(){e(h)})});g.click(function(){if(c&&c.selectionMode=="single"){$(d).each(function(){if($(this)!==g){b($(this))}})}if(!$(this).hasClass("toggled")){f($(this))}else{b($(this))}})});return $(this)};


