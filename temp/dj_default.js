$(document).ready(function(){
	//pageMain.init();

	var submenuTimeout;

	//신규방식
	/*
	$('div.Gnb ul.gnbMenu li.1Depth > a').on('mouseenter focusin', function(){
		$('div.Gnb ul.gnbMenu li.List .subMenu').removeClass('active');
		$('.Gnb').addClass('sel');
		$('#allbg').fadeIn('1');
		clearTimeout(submenuTimeout);
		submenuTimeout = setTimeout(function() {
			$("div.Gnb ul.gnbMenu li.List .subMenu").addClass('active');
		}, 100);
	});

	$('div.Gnb').on('mouseleave', function(){
		clearTimeout(submenuTimeout);
		submenuTimeout = setTimeout(function() {
			$("div.Gnb ul.gnbMenu li.List .subMenu").removeClass('active');
			$('.Gnb').removeClass('sel');
			$('#allbg').fadeOut();
		}, 100);
	});

	$('li.2Depth.menu_53.Last > a').on('focusout', function(){
		clearTimeout(submenuTimeout);
		submenuTimeout = setTimeout(function() {
			$("div.Gnb ul.gnbMenu li.List .subMenu").removeClass('active');
			$('.Gnb').removeClass('sel');
			$('#allbg').fadeOut();
		}, 100);
	});
	*/


/*
	$('div.Gnb').on('mouseout focusout', function(){
		$('div.Gnb ul.gnbMenu li.List').removeClass('active');
		$('div.Gnb').removeClass('on');
	});
*/
	//기존방식
	/*
	$('div.Gnb ul.gnbMenu li.List, div.Gnb div.mask').on('mouseover focusin', function(){
		$('div.Gnb ul.gnbMenu li.List .subMenu').removeClass('active');
		$(this).addClass('active');
		$('div.Gnb').addClass('on');
		$('div.mask').show();
	});
	$('div.Gnb ul.gnbMenu li.List ul, div.Gnb div.mask').on('mouseout focusout', function(){
		clearTimeout(submenuTimeout);
		submenuTimeout = setTimeout(function() {
			$('div.Gnb ul.gnbMenu li.List  .subMenu').removeClass('active');
			$('div.Gnb').removeClass('on');
			$('div.mask').hide();
		}, 3000);
	});
	$('div.Gnb div.mask').hide();
	*/
/*
	$('div.Gnb ul.gnbMenu li.1Depth > a, div.Gnb, div.Gnb div.mask').on('mouseenter', function(){
		$('div.Gnb ul.gnbMenu li.List').removeClass('active');
		$(this).parent('li').addClass('active');
		$('div.Gnb').addClass('on');
		$('div.mask').show();
	});

	$('div.Gnb ul.gnbMenu li.1Depth > a, div.Gnb, div.Gnb div.mask').on('focusin', function(){
		$('div.Gnb ul.gnbMenu li.List').removeClass('active');
		$(this).parent('li').addClass('active');
		$('div.Gnb').addClass('on');
		$('div.mask').show();
	});
*/

	// GNB
	$(document).on('mouseenter', '.gnbMenu > li > a', function(){
		$('.gnbMenu li.active').removeClass('active');
		$(this).parent('li').addClass('active');
		$('div.mask').show();
	});

	$(document).on('focusin', '.gnbMenu > li > a', function(){
		$('.gnbMenu li.active').removeClass('active');
		$(this).parent('li').addClass('active');
		$('div.mask').show();
	});

	$(document).on('mouseleave', '.Gnb', function(){
		$('.gnbMenu .active').removeClass('active');
		$('div.mask').hide();
	});

	$('li.2Depth.menu_53.Last > a').on('focusout', function(){
		$('.gnbMenu .active').removeClass('active');
		$('div.mask').hide();
	});

	$(document).on('focusout', '.Gnb', function(){
		clearTimeout(submenuTimeout);
		submenuTimeout = setTimeout(function() {
			$('.gnbMenu .active').removeClass('active');
		}, 5000);
	});

	var popupZoneLength = $('div.popupZone ul').length;
	var popupZone;
	if (popupZoneLength > 0) {
		popupZone = $('div.popupZone ul').bxSlider({
			mode:'fade',
			auto:true,
			controls:true,
			autoHover:true,
			pagerType:'short',
			onSliderLoad:function(currentIndex) {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
				//$('.bx-wrapper').find('a').attr('tabindex', -1);
			},
			onSliderResize:function() {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
			},
			onSlideBefore:function() {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
			},
			onSlideAfter:function() {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
			},
			onSlideNext:function() {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
			},
			onSlidePrev:function() {
				var pager = $('div.popupZone div.bx-pager').text().split(' ');
				var pagerHtml = '<span class="blue">'+pager[0]+'</span>'+pager[1]+pager[2];
				$('div.popupZone span#pager').html(pager);
			}
		});
	}
	$('div.popupZone a.prev').on('click',function(){
		if(popupZone != null ){
			popupZone.goToPrevSlide();
		}
		return false;
	});
	$('div.popupZone a.next').on('click',function(){
		if(popupZone != null){
			popupZone.goToNextSlide();
		}
		return false;
	});
	$('div.popupZone a.stop').on('click',function(){
		if(popupZone != null){
			popupZone.stopAuto();
		}
		$(this).removeClass('active');
		$('div.popupZone a.play').addClass('active');
		return false;
	});
	$('div.popupZone a.play').on('click',function(){
		if(popupZone != null){
			popupZone.startAuto();
		}
		$(this).removeClass('active');
		$('div.popupZone a.stop').addClass('active');
		return false;
	});

	var bannerLength = $('div.bannerbox ul.bannerImg').length;
	var bannerWrap = $('div.banner');
	if(bannerWrap.hasClass('noAuto')){
		var autoType = false;
	}else{
		var autoType = true;
	}

	var bannerSlider;

	if (bannerLength > 0) {
		bannerSlider = $('div.bannerbox ul.bannerImg').bxSlider({
			slideWidth:167,
			speed:500,
			moveSlides:1,
			maxSlides:3,
			auto:autoType,
			autoHover:true,
			pager:false,
			controls:false,
			onSliderLoad: function(){
				//$('.bx-wrapper').find('a').attr('tabindex', -1);
			}
		});
	}

	$('div.bannerBtn a.prev').on('click',function(){
		if(bannerSlider != null ){
			bannerSlider.goToPrevSlide();
		}
		return false;
	});
	$('div.bannerBtn a.next').on('click',function(){
		if(bannerSlider != null){
			bannerSlider.goToNextSlide();
		}
		return false;
	});
	$('div.bannerBtn a.stop').on('click',function(){
		if(bannerSlider != null){
			bannerSlider.stopAuto();
		}
		$(this).removeClass('active');
		$('div.bannerBtn a.play').addClass('active');
		return false;
	});
	$('div.bannerBtn a.play').on('click',function(){
		if(bannerSlider != null){
			bannerSlider.startAuto();
		}
		$(this).removeClass('active');
		$('div.bannerBtn a.stop').addClass('active');
		return false;
	});

	var slider;
	if ($('div.rolling-box div.box ul').length > 0) {
		slider =  $('div.rolling-box div.box ul').bxSlider({
			mode:'fade', 
			controls: false,
			pager:true,
			touchEnabled: true,
			auto: true,
			autoHover: true,
			responsive: true,
			onSliderLoad: function(){
				$(".bx-clone").find("a").prop("tabIndex","-1");
			},
			onSlideAfter: function(){
				$(".bx-wrapper").children("li").each(function(){
					if($(this).attr("aria-hidden") == "false"){
						$(this).find("a").attr("tabIndex","0");
					}else{
						$(this).find("a").attr("tabIndex","-1");
					}
				});
			}
		});
	};

	$('div.rolling-box div.box ul').on('focusin', function(){
		slider.stopAuto();
	});
	$('div.rolling-box div.box ul > li > a').on('focusin',function(){
		slider.goToSlide(slider.getCurrentSlide());
	});
	$('div.rolling-box div.box ul').on('focusout', function(){
		slider.startAuto();
	});
	$('div.rolling-box div.box ul > li > a').on('focusout',function(){
		slider.startAuto();
	});

	$('div.rolling-box a.bx-prev').on('click',function(){
		if(slider != null ){
			slider.goToPrevSlide();
		}
		return false;
	});
	$('div.rolling-box a.bx-next').on('click',function(){
		if(slider != null){
			slider.goToNextSlide();
		}
		return false;
	});


	var bookSlider;
	if ($('div.book div.bookContent ul').length > 0) {
		bookSlider = $('div.book div.bookContent ul').bxSlider({
			slideMargin:0,
			auto: true,
			autoHover:true,
			maxSlides: 4,
			controls:false,
			pager:false,
			moveSlides:1,
			stopAutoOnClick: true,
			slideMargin: 0,
			onSliderLoad: function(){
				$(".bx-clone").find("a").prop("tabIndex","-1");
			},
			onSlideAfter: function(){
				$(".bx-wrapper").children("li").each(function(){
					if($(this).attr("aria-hidden") == "false"){
						$(this).find("a").attr("tabIndex","0");
					}else{
						$(this).find("a").attr("tabIndex","-1");
					}
				});
			}
		});
	}
	$('div.book div.bookContent ul').on('focusin', function(){
		bookSlider.stopAuto();
	});
	$('div.book div.bookContent ul > li > a').on('focusin',function(){
		bookSlider.goToSlide(bookSlider.getCurrentSlide());
	});
	$('div.book div.bookContent ul').on('focusout', function(){
		bookSlider.startAuto();
	});
	$('div.book div.bookContent ul > li > a').on('focusout',function(){
		bookSlider.startAuto();
	});

	$('div.book a.prev').on('click',function(){
		if(bookSlider != null ){
			bookSlider.goToPrevSlide();
		}
		return false;
	});
	$('div.book a.next').on('click',function(){
		if(bookSlider != null){
			bookSlider.goToNextSlide();
		}
		return false;
	});
	$('div.book a.stop').on('click',function(){
		if(bookSlider != null){
			bookSlider.stopAuto();
		}
		$(this).removeClass('active');
		$('div.bannerBtn a.play').addClass('active');
		return false;
	});
	$('div.book a.play').on('click',function(){
		if(bookSlider != null){
			bookSlider.startAuto();
		}
		$(this).removeClass('active');
		$('div.bannerBtn a.stop').addClass('active');
		return false;
	});




/*
	var boardSlider;
	if ($('div.libSelectBox2 ul').length > 0) {
		boardSlider = $('div.libSelectBox2 ul').bxSlider({
			slideWidth:70,
			speed:500,
			moveSlides:1,
			maxSlides:3,
			auto:true,
			autoHover:true,
			pager:false,
			controls:false
		});
	}
	$('div.libSelectBox2 div.left a.prev').on('click',function(){
		if(boardSlider != null ){
			boardSlider.goToPrevSlide();
		}
		return false;
	});
	$('div.libSelectBox2 div.right a.next').on('click',function(){
		if(boardSlider != null){
			boardSlider.goToNextSlide();
		}
		return false;
	});
*/

	// TAB
	$(document).on('click', '.tab .tit a', function(){
		var target = this.getAttribute('href').replace('#','');
		var $box = $(this).closest('.tab');

		$box.find('.active').removeClass('active');
		$(this).parent().addClass('active');

		$box.find('.cont').hide();
		$box.find('[data-tab="'+target+'"]').show();
	});

	$(document).on('click', '.tabs .tit a', function(){
		var target = this.getAttribute('href').replace('#','');
		var $box = $(this).closest('.tabs');
		
		$box.find('.active').removeClass('active');
		$(this).parent().addClass('active');
		
		$('.tabs .tit a').attr('title','');
		$(this).attr('title','선택됨');
		
		$box.find('.cont').hide();
		$box.find('[data-tab="'+target+'"]').show();

		$('ul.t01').css('display','block');
		$('ul.t02').css('display','none');
		//$('ul.t03').css('display','none');
		$('ul.t04').css('display','none');
		$('ul.t05').css('display','none');
		$('ul.t06').css('display','none');
		$('ul.t07').css('display','none');
		$('ul.t08').css('display','none');
		$('ul.t09').css('display','none');
		$('ul.t10').css('display','none');
		$('ul.t11').css('display','none');
		$('ul.t12').css('display','none');
		
		$('.libSelectBox2 a.allLib').addClass('on');
		$('.libSelectBox2 a.youngsam').removeClass('on');
		$('.libSelectBox2 a.sadang').removeClass('on');
		//$('.libSelectBox2 a.sangdo').removeClass('on');
		$('.libSelectBox2 a.children').removeClass('on');
		$('.libSelectBox2 a.daebang').removeClass('on');
		$('.libSelectBox2 a.samter').removeClass('on');
		$('.libSelectBox2 a.yaksu').removeClass('on');
		$('.libSelectBox2 a.dawool').removeClass('on');
		$('.libSelectBox2 a.kuksabong').removeClass('on');
		$('.libSelectBox2 a.kkamang').removeClass('on');
		$('.libSelectBox2 a.sindaebang').removeClass('on');
		
		$('.libSelectBox2 a').attr('title','');
		$('a.allLib').attr('title','선택됨');
	});

	$('div.notice a.tab').on('click', function(e) {
		e.preventDefault();
		$('div.notice ul.title li').removeClass('on');
		$(this).parent().addClass('on');
		$('div.notice ul.list').removeClass('on');
		$('div.notice ul.list.'+$(this).data('tab')).addClass('on');
		$('li.lastLi a#boardMore').attr('href', $('div.notice ul.list.' + $(this).data('tab')).data('link'));
	});



	$('div.tab-menu > ul > li > a, div.tablink > ul > li > a, div.tabmenu.on > ul > li > a').on('click',function(e){
		e.preventDefault();
		if(!($(this).parent().hasClass('active'))){
			$(this).parents('ul').children().removeClass('active');
			$(this).parent().parent().parent().parent().children('div.tabCon').removeClass('active');
			$(this).parent().addClass('active');
			var activeTab = $(this).attr('href');
			$(activeTab).addClass('active');
		}
	});

	$('#footer .site1 .movebtn').click(function(e){
		var url=$('.site1 select option:selected').val();
		if (url == '') {
			alert('이동할 사이트를 선택해주세요');
			return false;
		}
		var openNewWindow = window.open("about:blank");
		openNewWindow.location.href=url;

		e.preventDefault();
	});$('#footer .site2 .movebtn').click(function(e){
		var url=$('.site2 select option:selected').val();
		if (url == '') {
			alert('이동할 사이트를 선택해주세요');
			return false;
		}
		var openNewWindow = window.open("about:blank");
		openNewWindow.location.href=url;

		e.preventDefault();
	});

});


var pageMain = (function(){
	var init;

	return {
		init: init
	}
})();