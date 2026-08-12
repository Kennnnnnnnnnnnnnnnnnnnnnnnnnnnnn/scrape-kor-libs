$(document).ready(function () {
	$(".btn_category").on("click", function (e) {
		if (!$(this).hasClass("act")) {
			// hide any open menus and remove all other classes
			$(".searchCategory .tree_wrap").slideUp(350);
			$(this).addClass("act");
		} else {
			// open our new menu and add the open class
			$(".searchCategory .tree_wrap").slideDown(350);
			$(this).removeClass("act");
		}
	});

	// 상세 간략/서지/MARC 보기 버튼
	$(".btn_optionView").on("click", function (e) {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
		} else if ($(this).hasClass("on")) {
			$(this).removeClass("on");
		}
	});

	$(".bookEventWrap a").focusin(function () {
		$(".btn_optionView").removeClass("on");
	});

	// 상세 간략정보 view/hide
	$(".list_optionView li.simpleLink a").on("click", function () {
		$(".btn_optionView").removeClass("on");
		$(".sergeView").removeClass("open");
		$(".marcWrap").removeClass("open");
		$(".simpleView").addClass("open");
	});
	// 상세 서지정보 view/hide
	$(".list_optionView li.sergeLink a").on("click", function () {
		$(".marcWrap").removeClass("open");
		$(".simpleView").removeClass("open");
		$(".sergeView").addClass("open");
		$(".btn_optionView").removeClass("on");
	});
	// 상세 MARC view/hide
	$(".list_optionView li.marcLink a").on("click", function () {
		$(".simpleView").removeClass("open");
		$(".sergeView").removeClass("open");
		$(".marcWrap").addClass("open");
		$(".btn_optionView").removeClass("on");
	});


	$(".ico_heart").on("click", function (e) {
		if ($(this).parent().has("span")) {
			e.preventDefault();
		}

		if (!$(this).hasClass("active")) {
			$(this).addClass("active");
		} else if ($(this).hasClass("active")) {
			$(this).removeClass("active");
		}
	});



	// Tab
	$(".searchUtilWrap ol li a, .searchUtilMenu li a").on("click", function () {
		var activeTab = $(this).attr("data-tab");
		$(".searchUtilWrap ol li a, .searchUtilMenu li a").attr("title", "축소됨");
		
		if (!$(this).hasClass("on")) {
			$(".searchUtilWrap ol li a, .searchUtilMenu li a").removeClass("on");
			$(this).addClass("on");
			$(this).attr("title", "확장됨");
			$(".divSelect").removeClass("current");
			$("#" + activeTab).addClass("current");
			$('.language li:first-child a').focus();
		} else {
			$(this).removeClass("on");
			$(this).attr("title", "축소됨");
			$("#" + activeTab).removeClass("current");
		}
	});

	$(".mobPasit").on("click", function () {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
			$(".finder_area").addClass("open");
		} else {
			$(this).removeClass("on");
			$(".finder_area").removeClass("open");
		}
		$("#container.sub").css("z-index", "999");
	});

	$(".finder_area .pasit_dim").on("click", function () {
		$(".mobPasit").removeClass("on");
		$(".finder_area").removeClass("open");
		$("#container.sub").css("z-index", "0");
	});


	$(window).on("resize orientationchange", function () {
		var width = parseInt($(this).width());
		if (width < 600) {
			$(".finder_tit, .btn_extend ").on("click", function () {
				if (!$(this).parents("._filter_row").hasClass("on")) {
					$(this).parents("._filter_row").addClass("on");
				} else {
					$(this).parents("._filter_row").removeClass("on");
				}
			});
		}
		if (width > 600) {
			$("_filter_row").removeClass("on");
		}
	}).resize();


	// 소장정보 view/hide
	$(".btn_haveInfo").on("click", function () {
		$(".whereLibrary").removeClass("open");
		$(".bibliographicInfo").removeClass("open");
		$(".btn_sergeInfo").removeClass("on");
		if (!$(this).hasClass("on")) {
			$(".btn_haveInfo").removeClass("on");
			$(this).addClass("on");
			$(this).parents("li").children(".whereLibrary").addClass("open").attr("tabIndex", "0").focus();
			$(this).attr("title", "소장정보 확장됨");
		} else {
			$(this).removeClass("on");
			$(".whereLibrary").removeClass("open").removeAttr("tabIndex", "0");
			$(this).attr("title", "소장정보 축소됨");
		}
	});
	// 서지정보 view/hide
	$(".btn_sergeInfo").on("click", function () {
		$(".whereLibrary").removeClass("open");
		$(".bibliographicInfo").removeClass("open");
		$(".btn_haveInfo, .btn_bkdanbi").removeClass("on");
		if (!$(this).hasClass("on")) {
			$(".btn_sergeInfo").removeClass("on");
			$(this).addClass("on");
			$(this).parents("li").children(".bibliographicInfo").addClass("open").attr("tabIndex", "0").focus();
			$(this).attr("title", "서지정보 확장됨");
		} else {
			$(this).removeClass("on");
			$(".bibliographicInfo").removeClass("open").removeAttr("tabIndex", "0");
			$(this).attr("title", "서지정보 축소됨");
		}
	});

	/* 검색결과 리스트/카드 형식 */
	if ($(".listTypeList").hasClass("on")) {
		$(".bookList").removeClass("cardViewStyle");
		$(".mobListType").removeClass("listTypeCard")
		$(".bookList").addClass("listViewStyle");
		$(".mobListType").addClass("listTypeList");
	}
	if ($(".listTypeCard").hasClass("on")) {
		$(".bookList").removeClass("listViewStyle");
		$(".mobListType").removeClass("listTypeList")
		$(".bookList").addClass("cardViewStyle");
		$(".mobListType").addClass("listTypeCard");
	}

	// 검색히스토리 레이어 팝업
	$(".help_icon").on("click", function () {
		$(".searchHistory").addClass("open");
	});


	$(".searchHistory .thispopClose").on("click", function () {
		$(".searchHistory").removeClass("open");
	});

	$(".dimLayerPop .thispopClose").on("click", function () {
		$(this).parents(".dimLayerPop").removeClass("open");
	});

	$(".btn_bookdanbi").on("click", function () {
		$(".bookDanbilyPop").addClass("open");
	});

	$(".helpLayerPop").on("click", function () {
		$(".mobLibraryInfo").addClass("open");
	});



	// 모바일 추천검색어 view/hide
	$(".recommendWrap .thisdrop").on("click", function () {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
			$(".recommendWrap").addClass("open");
		} else {
			$(this).removeClass("on");
			$(".recommendWrap").removeClass("open");
		}
	});
	// recommendWrap thisdrop

	// 모바일 하위 메뉴 view/hide
	$(".lowDepthSlide").on("click", function () {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
			$(".searchUtilMenu").addClass("open");
		} else {
			$(this).removeClass("on");
			$(".searchUtilMenu").removeClass("open");
		}
	});



	$(".HanChange span").on("click", function () {
		var bname = $(this).data("name");
		$(".HanChange span").removeAttr("title");
		if (!$(this).hasClass("on")) {
			$(this).siblings("span").removeClass("on");
			$(".book_name").removeClass("on");
			$(".book_dataInner li.kor").removeClass("on");
			$(".book_dataInner li.han").removeClass("on");
			$(this).addClass("on");
			$(".book_name." + bname).addClass("on");
			$(".book_dataInner li." + bname).addClass("on");
		} else {
			$(this).attr("title", "선택됨");
		}
	});



	// 인기도서 모바일용 리스트 타입 버튼
	$(".mobinterestListType").on("click", function () {
		if ($(this).hasClass("listTypeCard")) {
			$(this).removeClass("listTypeCard");
			$(this).addClass("listTypeList");
			$(".qrationBookList").addClass("listViewStyle");
		} else {
			$(this).removeClass("listTypeList");
			$(this).addClass("listTypeCard");
			$(".qrationBookList").removeClass("listViewStyle");
		}
	});

	// 모바일용 리스트 타입 버튼
	$(".btnSetmob .mobListType").on("click", function () {
		if ($(this).hasClass("listTypeList")) {
			$(this).removeClass("listTypeList");
			$(this).addClass("listTypeCard");

			$(".btnSetWeb .listTypeList").removeClass("on");
			$(".btnSetWeb .listTypeCard").addClass("on");
			$(".bookList").removeClass("listViewStyle");
			$(".bookList").addClass("cardViewStyle");
		} else if ($(this).hasClass("listTypeCard")) {
			$(this).removeClass("listTypeCard");
			$(this).addClass("listTypeList");

			$(".btnSetWeb .listTypeCard").removeClass("on");
			$(".btnSetWeb .listTypeList").addClass("on");
			$(".bookList").removeClass("cardViewStyle");
			$(".bookList").addClass("listViewStyle");
		}
	});

	$(".btnSetWeb .listTypeList").on("click", function () {
		$(".bookList").removeClass("cardViewStyle");
		$(".bookList").addClass("listViewStyle");
		$(".listTypeCard").removeClass("on").removeAttr("title");
		$(this).addClass("on");
		$(this).attr("title", "선택됨");

		$(".btnSetmob .mobListType").removeClass("listTypeCard");
		$(".btnSetmob .mobListType").addClass("listTypeList");
	});

	$(".btnSetWeb .listTypeCard").on("click", function () {
		$(".bookList").removeClass("listViewStyle");
		$(".bookList").addClass("cardViewStyle");
		$(".listTypeList").removeClass("on").removeAttr("title");
		$(this).addClass("on");
		$(this).attr("title", "선택됨");

		$(".btnSetmob .mobListType").removeClass("listTypeList");
		$(".btnSetmob .mobListType").addClass("listTypeCard");

		// 카드형 리스트 포커스시 내용 보여지기
		$('.cardViewStyle .bookImg a').focusin(function(){
			$(this).parents("li").siblings("li").removeClass('on');
			$(this).parents("li").addClass('on');
		});
		$('.cardViewStyle .bookDetailInfo a').focusout(function(){
			$('.cardViewStyle ul li').removeClass('on');
		});
	});

	// Tab
	$("ul.tab_list li").click(function () {
		var activeTab = $(this).attr("data-tab");
		$("ul.tab_list li").removeClass("current");
		$(".tabWrap").removeClass("current");
		$(this).addClass("current");
		$("#" + activeTab).addClass("current");
	})

	//입력 없으면 최근&인기 있으면 자동완성
	/* $(".searchInputbox input:first-child").on("click", function(){
	  if($("#totalSearchValue").val() == "" || $("#totalSearchValue").val() == null ){
		$(".tab_wrap_search").addClass("open");
		$(".autoSearch").removeClass("open");
		return false; //중요
	  }
	  else {
		//$(".autoSearch").addClass("open");
		return false; //중요
	  }
   });*/

	//공유하기 팝업 외에 영역 클릭
	$(document).click(function (e) { //문서 body를 클릭했을때
		if (e.target.className == "tab_wrap_search") {
			return false
		}
		$(".tab_wrap_search").removeClass("open");
	});

	//자동완성
	$(".searchInputbox input:first-child").on("click propertychange change keyup input", function () {
		if ($("#totalSearchValue").val() == "" || $("#totalSearchValue").val() == null) {
			$(".autoSearch").removeClass("open");
			$(".tab_wrap_search").addClass("open");
			return false; //중요
		} else {
			$(".autoSearch").addClass("open");
			$(".tab_wrap_search").removeClass("open");
			return false; //중요
		}
	});
	//자동완성 외에 영역 클릭
	$(document).click(function (e) { //문서 body를 클릭했을때
		if (e.target.className == "autoSearch") {
			return false
		}
		$(".autoSearch").removeClass("open");
	});

	// 소장정보 모바일
	$(".mobHaveBookLibrary dt").on("click", function () {
		if (!$(this).hasClass("on")) {
			$(".mobHaveBookLibrary dt").removeClass("on");
			$(this).addClass("on");
		} else {
			$(this).removeClass("on");
		}
	});

	// 책소개 더보기 버튼
	var $wrap = $("#wrap");
	var mobileChk = ($wrap.width() < 640) ? true : false;
	if (mobileChk) {
		var bookInfoH = $(".bookInformation").height();
		if (bookInfoH > 100) {
			$(".mobMoreView").show();
			$(".bookInformation").css("height", "100px");
		} else {
			$(".mobMoreView").hide();
			$(".bookInformation").css("height", "auto");
		}
	}

	$(".mobMoreView").on("click", function () {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
			$(".bookInformation").css("height", "auto");
		} else {
			$(this).removeClass("on");
			$(".bookInformation").css("height", "100px");
		}
	});

	//최근, 인기검색어 탭
	$(".tab_wrap_search ul.tab li").click(function () {
		$(".tab_wrap_search ul.tab li").removeClass("on");
		$(this).addClass("on");
		var tabIndex = $(".tab_wrap_search ul.tab li").index($(this));
		$(".tab_wrap_search .tab_con .popular_search").hide();
		$(".tab_wrap_search .tab_con .popular_search").eq(tabIndex).show();
		return false;
	});

	$(".recent_delete").click(function () {
		$(".tab_wrap_search .tab_con .p1 li").css("display", "none");
		$(".tab_wrap_search .tab_con .p1 li.none").css("display", "block");
		return false;

	});
	//검색어 저장 버튼
	$(".save_off").click(function () {
		if (!$(this).hasClass("on")) {
			$(this).addClass("on");
			$(this).text("검색어저장 끄기");
			$(".tab_wrap_search .tab_con .p1 li").css("display", "block");
			$(".tab_wrap_search .tab_con .p1 li.none").css("display", "none");
			$(".tab_wrap_search .tab_con .p1 li.off").css("display", "none");
			return false;
		} else {
			$(this).removeClass("on");
			$(this).text("검색어저장 켜기");
			$(".tab_wrap_search .tab_con .p1 li").css("display", "none");
			$(".tab_wrap_search .tab_con .p1 li.off").css("display", "block");
			return false;
		}
	});

	$(".save_off").focusout(function () {
		$(".tab_wrap_search").removeClass("open");
	});


	$(".worldwordBox .worldword ul.language li:first-child a").trigger("click");
	//다국어입력기
	$(".worldwordBox .worldword ul.language li a").click(function () {
		$(".worldwordBox .worldword ul.language li a").hasClass("selected");
		$(".worldwordBox .worldword ul.language li a").removeClass("selected");
		$(this).addClass("selected");
		var multiLangIndex = $(".worldwordBox .worldword ul.language li a").index($(this));
		$(".worldwordBox .worldword .languageContents").hide();
		$(".worldwordBox .worldword .languageContents").eq(multiLangIndex).show();
		return false;
	});
	$(".worldwordBox .worldword ul.language li:first-child a").trigger("click");

	// 이미지형 리스트 포커스시 내용 보여지기
	$('.qrationBookList .bookImg a').focusin(function(){
		$(this).parents("li").siblings("li").removeClass('on');
		$(this).parents("li").addClass('on');
	});
	$('.qrationBookList .bookEventWrap a.btn_sergeInfo').focusout(function(){
		$('.qrationBookList ul li').removeClass('on');
	});

	// searchInputbox
	// tab_wrap_search

	//연속간행물 - 권호정보
	/*$(".dropBookData #dataInfo").on("click", function(){
	  if(!$(this).hasClass("on")) {
		$(this).addClass("on");
		$(this).parents("tr").siblings("tr").find("#dataInfo").removeClass("on");
		$(".dropBookData.dataInfo").addClass("open");
	  } else {
		$(this).removeClass("on");
		$(".dropBookData.dataInfo").removeClass("open");
	  }
	});*/

	//함께 비치된 도서
	/* var basicVal = $(".recommendLibrary select option:selected").val();
	$(".swiper01").css("display","none");
	$(".swiper01." + basicVal).css("display","block");
	$(".recommendLibrary select").on("change", function(){
	  bookChange(this);
	});
	function bookChange(o){
	  var val = $(":selected", o).val(); // 전달받은 "셀렉트박스 요소" 에서 선택된 것 찾기
	  $(".swiper01").css("display","none");
	  $(".swiper01." + val).css("display","block");
	}*/

	//권호정보
	/*var basicVal = $(".recommendLibrary select option:selected").val();
	$(".recommendLibrary + .tblWrap tbody tr").css("display","none");
	$(".recommendLibrary + .tblWrap tbody tr." + basicVal).css("display","table-row");
	$(".recommendLibrary select").on("change", function(){
	  tblChange(this);
	});
	function tblChange(o){
	  var val = $(":selected", o).val(); // 전달받은 "셀렉트박스 요소" 에서 선택된 것 찾기
	  $(".recommendLibrary + .tblWrap tbody tr").css("display","none");
	  $(".recommendLibrary + .tblWrap tbody tr." + val).css("display","table-row");
	}*/
});