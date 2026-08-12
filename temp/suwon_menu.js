/**
 * Filename : menu.js
 * @author  : 강정민
 * @Description: 메뉴   최신버전
 */

/**
 * name : 메뉴명(타이틀로도 사용)
 * url : url
 * menuClass : body 태그 class로 지정됨
 * submenu : 하위메뉴
 * level: 2인경우 메뉴바에 호출 안됨 
 */
var menuList = [
    {
    	"name":"자료검색",
    	"url":"/search",
    	"menuClass" : "search",
    	"submenu":[
            {	
            	"name":"자료검색",
            	"url":"/search",
            	"menuClass" : "",
		     },
        ]
    },
    {
        "name":"큐레이션",
    	"url":"",
    	"menuClass" : "curation",
    	"submenu":[
            {
            	"name":"신착도서",
		     	"url":"/curation/arrival",
		        "menuClass" : "newBook"
		     },
		     {
	        	"name":"인기도서",
		     	"url":"/curation/best",
		     	"menuClass" : "bestBook"
		     },
		     {
	        	"name":"추천도서",
		     	"url":"/curation/recommend",
		     	"menuClass" : "recommen"
		     }
			,
			{
				"name":"자료탐색",
				"url":"/curation/category",
				"menuClass" : "category",
			}
        ]
    },
	{
		"name":"전자도서관",
		"url":"",
		"menuClass" : "ebook",
		"submenu":[
			{
				"name":"전자도서관",
				"url":"https://ebook.suwonlib.go.kr/elibrary-front/main.ink",
				"menuClass" : ""
			}
		]
	},

	{
		"name":"지역도서관 통합검색",
		"url":"",
		"menuClass" : "local",
		"submenu":[
			{
				"name":"지역도서관 통합검색",
				"url":"/localSearch",
				"menuClass" : "",
			}
		]
	},
    /*{
        "name":"도서관이용",
    	"url":"",
    	"menuClass" : "libintro",
    	"submenu":[
            {
            	"name":"이용안내",
		     	"url":"/libIntro/introduction",
                "level":"1",
             	"menuClass" : "intro"
		     },
            {
            	"name":"공지사항",
		     	"url":"/notice",
                "level":"1",
		     	"menuClass" : "notice"
		     }
        ]
    },*/
	{
		"name":"나의도서관",
		"url":"",
		"menuClass":"mylib",
		"submenu":[
			{
				"name":"내책장",
				"url":"/myLibrary/myBookCase",
				"level":"1",
				"menuClass":"myBookCase"
			},
			{
				"name":"희망도서신청",
				"url":"/myLibrary/hopeBookApply",
				"level":"1",
				"menuClass":"hopeBookApply"
			},
			{
				"name":"서점 바로대출 신청",
				"url":"/myLibrary/hopeBookInstantApplyGuide",
				"level":"1",
				"menuClass":"hopeBookInstantApplyGuide",
			},
			{
				"name":"서점 바로대출 신청",
				"url":"/myLibrary/hopeBookInstantApply",
				"level":"4",
				"menuClass":"hopeBookInstantApplyGuide"
			},
		]
	},
	{
		"name":"내서재",
		"url":"",
		"level":"2",
		"menuClass" : "member",
		"submenu":[
			{
				"name":"대출",
				"url":"/myLibrary/loanStatus",
				"level":"1",
				"menuClass" : "loanStatus"
			},
			{
				"name":"대출",
				"url":"/myLibrary/history",
				"level":"4",
				"menuClass" : "loanStatus"
			},
			{
				"name":"일반예약",
				"url":"/myLibrary/reserveList",
				"level":"1",
				"menuClass" : "reservList"
			},
			{
				"name":"책나루<br class='block'>(무인)",
				"url":"/myLibrary/unmannedReserveList",
				"level":"1",
				"menuClass" : "unmannedReserveList"
			},
			{
				"name":"상호대차",
				"url":"/myLibrary/lill",
				"level":"1",
				"menuClass" : "lill"
			},
			{
				"name":"희망도서",
				"url":"/myLibrary/hopeBooks",
				"level":"1",
				"menuClass" : "hopeBooks"
			},
			{
				"name":"희망도서",
				"url":"/myLibrary/hopeInstantBooks",
				"level":"4",
				"menuClass" : "hopeBooks"
			},
		]
	},
/*    {
        "name":"마이페이지",
    	"url":"",
        "level":"2",
    	"menuClass" : "member",
    	"submenu":[
            {
            	"name":"내정보수정",
		     	"url":"/myPage/modify",
                "level":"2",
             	"menuClass" : "modify"
            },
            {
            	"name":"약관재동의",
		     	"url":"/myPage/reagree",
                "level":"2",
             	"menuClass" : "reagree"
            },
            {
            	"name":"회원탈퇴",
		     	"url":"/myPage/withdrawal",
                "level":"2",
             	"menuClass" : "withdrawal"
            },
        ]
    },*/
    {
    	"name":"이용약관",
     	"url":"/terms/termsOfUsePage",
        "level":"2",
     	"menuClass" : "member terms"
    },
    {
    	"name":"개인정보처리방침",
     	"url":"/privacyPolicy/privacyPolicyPage",
        "level":"2",
     	"menuClass" : "member personalInfo"
    },
    {
    	"name":"이메일무단수집여부",
     	"url":"/emailWithoutWhether/emailWithoutWhetherPage",
        "level":"2",
     	"menuClass" : "member email"
    }
];



/**
 * writeMenu :  메뉴생성 함수
 * @author 강정민
 */
function writeMenu() {
	//정리 필요.
	var homeImg = "<li class=\"location_home\"><img src=\""+getContextPath()+"/images/sub/ico_location_home.png\" alt=\"홈\"></li>";
	var jsonObj = menuList;
	var menuHTML = "";
	var levelChk = true;
	var menuClass = "";
	var menuTitle = "수원시도서관 모바일";
	var subTit = "";
	var contHeaderHtml = "";
	var subTabBtn = "";
	var jsonTabObj = "";
	let nowMenuClass = "";
	for (var key in jsonObj) {
		if(jsonObj[key].level !="2"){
			menuHTML += "<li><a href='#'><span>"+jsonObj[key].name+"</span></a><ul>";
			for (let subkey in jsonObj[key].submenu) {
				subTabBtn += ""
				if( ((jsonObj[key].submenu[subkey].menuClass === "delivery" && getStaffCheck() === "Y") || jsonObj[key].submenu[subkey].menuClass != "delivery")){
					if((jsonObj[key].submenu[subkey].menuClass === "lill" && getLillStaffCheck() == "Y") || jsonObj[key].submenu[subkey].menuClass != "lill"){
						if(jsonObj[key].submenu[subkey].name.indexOf("전자도서관") !== -1){
							if(!isNullCheck(login_id) && !isNullCheck(login_name)){
								if (login_user_no == null || login_user_no == "" || login_memberClass == "2") {
									menuHTML += "<li><a href=\"\" onclick=\"openWebUserChkPop(); return false;\">"+jsonObj[key].submenu[subkey].name+"</a></li>";
								} else {
									menuHTML += "<li><a href=\"https://ebook.suwonlib.go.kr/elibrary-front/frontapi/mmbrLnkg.ink?param_1=" + login_id + "&param_3=" + login_name + "&libraryCode=20086\" target=\"_blank\" onclick=\"insertMenuLog('전자도서관')\">" + jsonObj[key].submenu[subkey].name + "</a></li>";
								}
							} else {
								menuHTML += "<li><a href=\"\" onclick=\"alert('로그인이 필요한 서비스입니다.'); return false;\">"+jsonObj[key].submenu[subkey].name+"</a></li>";
							}
						} else if(jsonObj[key].submenu[subkey].level != "2" && jsonObj[key].submenu[subkey].level != "4"){
							menuHTML += "<li><a href=\"#\" onclick=\"goMenuPage('"+jsonObj[key].submenu[subkey].url + "'); return false;\">"+jsonObj[key].submenu[subkey].name+"</a></li>";
						}
						
						if(window.location.pathname.indexOf(jsonObj[key].submenu[subkey].url) !== -1){
							jsonTabObj = jsonObj[key];
							//subTit += "<h3 class=\"sub_tit\">"+jsonObj[key].name+"</h3>";
							subTit = "<h3 class=\"sub_tit\">"+jsonObj[key].name+"</h3>";
							menuClass = jsonObj[key].menuClass + " " +jsonObj[key].submenu[subkey].menuClass;
							nowMenuClass = jsonObj[key].menuClass;
							menuTitle = jsonObj[key].name + " > " +jsonObj[key].submenu[subkey].name + " : 수원시도서관 모바일";
							if(jsonObj[key].submenu[subkey].name === jsonObj[key].name){
								contHeaderHtml = homeImg + "<li class=\"loction_arrow\"></li><li>"+jsonObj[key].name+"</li>";	
							} else {
								contHeaderHtml = homeImg + "<li class=\"loction_arrow\"></li><li>"+jsonObj[key].name+"</li><li class=\"loction_arrow\"></li><li>"+jsonObj[key].submenu[subkey].name+"</li>";
							}
							
						}	
					}
				}
			}
		} else {
			if(isNullCheck(jsonObj[key].submenu)){
				if(window.location.pathname.indexOf(jsonObj[key].url) !== -1){
					subTit += "<h3 class=\"sub_tit\">"+jsonObj[key].name+"</h3>";
					contHeaderHtml = homeImg + "<li class=\"loction_arrow\"></li><li>"+jsonObj[key].name+"</li>";
					menuTitle = jsonObj[key].name  + ": 수원시도서관 모바일";
					menuClass = jsonObj[key].menuClass;
					nowMenuClass = jsonObj[key].menuClass;
				}
			} else {
				for (var subkey in jsonObj[key].submenu) {
					if(window.location.pathname.indexOf(jsonObj[key].submenu[subkey].url) !== -1){
						jsonTabObj = jsonObj[key];
						subTit += "<h3 class=\"sub_tit\">"+jsonObj[key].name+"</h3>";
						menuClass = jsonObj[key].menuClass + " " +jsonObj[key].submenu[subkey].menuClass;
						nowMenuClass = jsonObj[key].menuClass;
						menuTitle = jsonObj[key].name + " > " +jsonObj[key].submenu[subkey].name + " : 수원시도서관 모바일";
						contHeaderHtml = homeImg + "<li class=\"loction_arrow\"></li><li>"+jsonObj[key].name+"</li><li class=\"loction_arrow\"></li><li>"+jsonObj[key].submenu[subkey].name+"</li>";
					}
				}
			}
		}
		menuHTML += "</ul></li>";
	}
	
	// 탭메뉴 생성
	if(!isNullCheck(jsonTabObj) && !isNullCheck(jsonTabObj.submenu)){
		let tabManuHtml = "";
		let tabMoManuHtml = "";
		let tabMobileHtml = "";
		let tabUrl = "";
		let tabMenuClass = "";
		for (let subkey in jsonTabObj.submenu) {
			if(jsonTabObj.submenu[subkey].level != "3" && ((jsonTabObj.submenu[subkey].menuClass === "delivery" && getStaffCheck() === "Y") || jsonTabObj.submenu[subkey].menuClass != "delivery")){

				if((jsonTabObj.submenu[subkey].menuClass === "lill" && getLillStaffCheck() == "Y") || jsonTabObj.submenu[subkey].menuClass != "lill"){
					tabUrl = jsonTabObj.submenu[subkey].url;
					if(jsonTabObj.submenu[subkey].menuClass == "join"){
						tabUrl = tabUrl + "/step_01";
					}
					if(jsonTabObj.submenu[subkey].level != "4") {
						if (window.location.pathname.indexOf(jsonTabObj.submenu[subkey].url) !== -1
							|| (window.location.pathname.indexOf("/myLibrary/history") !== -1 && jsonTabObj.submenu[subkey].menuClass=="loanStatus")
							|| (window.location.pathname.indexOf("/myLibrary/hopeInstantBooks") !== -1 && jsonTabObj.submenu[subkey].menuClass=="hopeBooks")
							|| (window.location.pathname.indexOf("/myLibrary/hopeBookInstantApply") !== -1 && jsonTabObj.submenu[subkey].menuClass=="hopeBookInstantApplyGuide")
						) {
							tabMenuClass = jsonTabObj.submenu[subkey].menuClass;
							if(jsonTabObj.submenu[subkey].menuClass == "unmannedReserveList"){
								tabMobileHtml = '<div class="mobileTabmenu"><span class="selectMobile">책나루<br class="mobile">(무인)</span></div>';
								tabManuHtml += "<li class=\"on\"><a href=\"#" + jsonTabObj.submenu[subkey].menuClass + "\" onclick=\"goMenuPage('" + tabUrl + "'); return false;\">책나루<br class=\"block\">(무인)</a></li>";
							} else {
								tabMobileHtml = '<div class="mobileTabmenu"><span class="selectMobile">' + jsonTabObj.submenu[subkey].name + '</span></div>';
								tabManuHtml += "<li class=\"on\"><a href=\"#" + jsonTabObj.submenu[subkey].menuClass + "\" onclick=\"goMenuPage('" + tabUrl + "'); return false;\">" + jsonTabObj.submenu[subkey].name + "</a></li>";
							}

							tabMoManuHtml = "<a href=\"#none\">" + jsonTabObj.submenu[subkey].name + "</a>";
						} else {
							tabManuHtml += "<li><a href=\"#" + jsonTabObj.submenu[subkey].menuClass + "\" onclick=\"goMenuPage('" + tabUrl + "'); return false;\">" + jsonTabObj.submenu[subkey].name + "</a></li>";
						}
					}
				}
			}

		}
		if(!isNullCheck(tabManuHtml)){
			if(nowMenuClass == "member" || nowMenuClass == "mylib"){
				$(".menulink01").html( tabManuHtml );
			} else {
				$("#topTabMenuDiv").html(tabMobileHtml +"<ul>"+tabManuHtml+"</ul>");
				$(".menulink01").html(tabMoManuHtml + "<ul class=\"menulink01_01\">" + tabManuHtml + "</ul>");
			}
		}
	
	}
	
	
	//해더 메뉴 생성
	$("#menuArea").html(menuHTML);
	
	// body 태그 메뉴에 따라 클래서 변경
	$("body").removeClass();
	$("body").addClass(menuClass);

	// 타이틀 재설정
	$("title").html(menuTitle);
	
	if(!isNullCheck(contHeaderHtml)){
		//subTop 부분 생성
		contHeaderHtml = "<div class=\"inner\">" + subTit +"<div class=\"location\"><ul>" + contHeaderHtml + "</ul></div></div>";
		$(".subTop").html(contHeaderHtml);
	}
	
	setMenuClick();
}

function getDeviceType() {
	const ua = navigator.userAgent;
	if (/Mobi|Android|iPhone|iPad|iPod/i.test(ua)) {
		return "MOBILE";
	}
	return "PC";
}

function insertMenuLog(menu1, menu2, menu3) {
	const deviceType = getDeviceType();

	commonAjaxRequest({
		method : 'get',
		url  : getContextPath()+'/log/insertLog',
		params : {
			"deviceType" : deviceType,
			"menu1" : menu1 || "",
			"menu2" : menu2 || "",
			"menu3" : menu3 || "",
		},
		success : function(data){
		}
	});
}

function insertFunctionLog(menu) {
	const deviceType = getDeviceType();

	commonAjaxRequest({
		method : 'get',
		url  : getContextPath()+'/log/insertFunctionLog',
		params : {
			"deviceType" : deviceType,
			"menu" : menu || "",
		},
		success : function(data){
		}
	});
}


/**
 * goDeliveryPage :  배달 페이지 접근 (직원 체크)
 *
 * @date 2022.02.28
 * @author kjm
 * @param menuUrl : 접근  url
 * @return  
 */
function goDeliveryPage(menuUrl){
	if(getStaffCheck() === "Y"){
		goMenuPage(menuUrl);
	} else {
		alert("직원만 접근 가능한 메뉴입니다.");
	}
	
}

 /**
  * goMenuPage :  메뉴 페이지 접근
  *
  * @date 2022.02.28
  * @author kjm
  * @param menuUrl : 접근  url
  * @return  
  */
function goMenuPage(menuUrl){

	 if (menuUrl === "/myLibrary/hopeBookInstantApply" && (isNullCheck(login_key) || isNullCheck(login_name))
	 ) {
		 alert("서점 바로대출 신청은 로그인 후 이용 가능합니다.");
		 return false;
	 }

	 var goMenuUrl = "";
	 var urlMangage = getManageCode();

	if(!isNullCheck(login_key) && !isNullCheck(login_name)) {
		if (menuUrl === "/myLibrary/loanStatus" || menuUrl === "/myLibrary/hopeBookApply" || menuUrl ===  "/myLibrary/myBookCase" || menuUrl === "/myLibrary/hopeBookInstantApply") {
			if (login_user_no == null || login_user_no == "" || login_memberClass == "2") {
				openWebUserChkPop();
				return false;
		 	}
	 	}
	}

	if(menuUrl == "main"){
		if(!isNullCheck(urlMangage)){
    		goMenuUrl = getContextPath() + "/" + urlMangage;
		} else {
    		goMenuUrl = getContextPath() + "/";
		}
	} else {
		if(!isNullCheck(urlMangage)){
    		goMenuUrl = getContextPath() + menuUrl +"/"+ urlMangage;
    	} else {
    		goMenuUrl = getContextPath() + menuUrl;
    	}	
	}
	var frm = document.createElement("form");
	frm.setAttribute("method","POST");
	frm.setAttribute("action",goMenuUrl);    	
	document.body.appendChild(frm);
	frm.submit(); 
}

/**
 * goContentsWithParam :  페이지 접근 (파라미터 포함)
 *
 * @date 2022.02.28
 * @author kjm
 * @param params : 전달 파라미터(파라미터명:값) , menuUrl : 접근  url
 * @return  
 */
function goContentsWithParam(params,menuUrl, methodType){
	let functionName = "통합검색";
	var goMenuUrl = "";
	var urlMangage = getManageCode();
	if(menuUrl == "main"){
		if(!isNullCheck(urlMangage)){
    		goMenuUrl = getContextPath() + "/" + urlMangage;
		} else {
    		goMenuUrl = getContextPath() + "/";
		}
	} else {
		if(!isNullCheck(urlMangage)){
    		goMenuUrl = getContextPath() + menuUrl +"/"+ urlMangage;
    	} else {
    		goMenuUrl = getContextPath() + menuUrl;
    	}	
	}
	
	if(isNullCheck(methodType)){
		methodType = "GET";
	}
	
	var frm = document.createElement("form");
	frm.setAttribute("method",methodType);
	frm.setAttribute("action", goMenuUrl);
	
	if(params != null){
    	let paramArr = params.split(",");
    	for(var i=0; i < paramArr.length; i++){
			let item = paramArr[i].trim();
			let colonIdx = item.indexOf(":");
			if(colonIdx === -1 || colonIdx === item.length - 1) continue;
			let name = item.substring(0, colonIdx);
			let value = item.substring(colonIdx + 1);
    		let param = document.createElement("input");
    		param.setAttribute("type","hidden");
    		param.setAttribute("name",name);
    		param.setAttribute("value",value);
    		frm.appendChild(param);
    	}
	}

	insertFunctionLog(functionName);
	
	document.body.appendChild(frm);
	frm.submit();
}

function setMenuClick(){

	$('#menuArea').on('mouseover', function(){
	 	widthChangeCss("on","com");
	});	
	$('#menuArea').on('mouseout', function(){
	 	widthChangeCss("off","com");
	}); // 모바일에서 는 on 유지
	$('#menuArea a').on('focus', function(){
	 	widthChangeCss("on","com");
	});	
	$('#menuArea a').on('blur', function(){
	 	widthChangeCss("off","com");
	});
	
	$('#menuArea li a').click(function() {
		var mobileChk = ($("body").width() <= 1025) ? true : false;
		$("#menuArea li").removeClass('on');
		if(mobileChk){
			$(this).parent("li").addClass('on',"com");
		}
	});
	
	//메뉴 햄버거 버튼 클릭 이벤트
	$("#menuCloseBtn").click(function() {
	 	widthChangeCss("off");
	});
	$("#menuOpenBtn").click(function() {
		widthChangeCss("on");
	});
    $("#menuCloseBtn span").click(function() {
	 	widthChangeCss("off");
	});
    $("#menuOpenBtn span").click(function() {
	 	widthChangeCss("on");
	});
}
