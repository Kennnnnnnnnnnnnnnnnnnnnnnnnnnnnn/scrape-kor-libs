/**
 * Common Js
 */
// Init
var readonlyHandler = function(e) {
	var key = "which" in e ? e.which : e.keyCode;
	if (key == 8) {
		e.preventDefault();
		return false;
	}
};
$(function(){
	$('a').attr('rel','noopener noreferrer');
  });

(function($){
	$(document).ready(function(){
		//readonly backspace 방지
		$("input[readonly]").bind("keydown", readonlyHandler);

		// 숫자만 입력
		$(".numeric").css("ime-mode", "disabled").keydown(function(e) {
			e = e || window.e;
			var key = (e.which) ? e.which : e.keyCode;
			if( !((key >= 48 && key <= 57 && !e.shiftKey) || (key >= 96 && key <= 105) ||
					key == 8 || key == 9 || key == 46 || key == 37 || key == 39 )){
				e.preventDefault();
				return false;
			}
		});

		$(".numeric").keyup(function(e) {
			var regexp = /[^0-9]/g;
			var v = this.value;
			this.value = v.replace(regexp,'');
		});
		$(".numeric").keydown(function(e) {
			var regexp = /[^0-9]/g;
			var v = this.value;
			this.value = v.replace(regexp,'');
		});
	});
}(jQuery));



//Null 체크
function isEmpty( val ){
	if(val==null || typeof(val) === 'undefined' || $.trim(val) == '') {
		return true;
	}
	return false;
}


function isNotEmpty(val){
	return !isEmpty(val);
}

//이메일 유효성 검사
function isValidEmail(val) {
	var regex=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/;
	if(regex.test(val) === false) {
		//alert("유효하지 않은 이메일입니다.");
		return false;
	}
	return true;
}

function isNotValidEmail(val) {
	return !isValidEmail(val);
}

function isValidTelNo(val) {
	var regex = /^\d{2,4}-\d{3,4}-\d{4}$/;
	if(regex.test(val) === false) {
		//alert('유효하지 않은 전화번호입니다.\n예) 02-123-1234 또는 011-123-1234 또는 012-1234-1234 또는 0123-1234-1234');
		return false;
	}
	return true;
}

function isNotValidTelNo(val) {
	return !isValidTelNo(val);
}

function isNotValidMobileNo(val) {
	return !isValidMobileNo(val);
}

function isValidMobileNo(val) {
	var regex = /^\d{3}-\d{3,4}-\d{4}$/;
	if(regex.test(val) === false) {
		//alert('유효하지 않은 휴대폰번호입니다.\n예) 011-123-1234 또는 011-1234-1234');
		return false;
	}
	return true;
}

//Url 인코딩
function fnEncode(unencoded) {
	return encodeURIComponent(unencoded).replace(/'/g,"%27").replace(/"/g,"%22");
}

//Url 디코딩
function fnDecode(encoded) {
	return decodeURIComponent(encoded.replace(/\+/g,  " "));
}
//주민번호 검증
function isValidSocialNo(val) {

	//주민등록 번호 13자리를 검사한다.
	var fmt = /^\d{6}[1234]\d{6}$/;  //포멧 설정
	if (!fmt.test(val)) {
		return false;
	}

	// 생년월일 검사
	var birthYear = (val.charAt(6) <= "2") ? "19" : "20";
	birthYear += val.substr(0, 2);
	var birthMonth = val.substr(2, 2) - 1;
	var birthDate = val.substr(4, 2);
	var birth = new Date(birthYear, birthMonth, birthDate);

	if ( birth.getYear() % 100 != val.substr(0, 2) ||
			birth.getMonth() != birthMonth ||
			birth.getDate() != birthDate) {
		return false;
	}

	// Check Sum 코드의 유효성 검사
	var buf = new Array(13);
	for (var i = 0; i < 13; i++) {buf[i] = parseInt(val.charAt(i));}

	multipliers = [2,3,4,5,6,7,8,9,2,3,4,5];
	for (var sum = 0, i = 0; i < 12; i++) {sum += (buf[i] *= multipliers[i]);}

	if ((11 - (sum % 11)) % 10 != buf[12]) {
		return false;
	}
	return true;
}

function isNotValidSocialNo(val) {
	return !isValidSocialNo(val);
}

//날짜 유효성 검사
function isValidDate(val)
{
	//숫자만 남김
	val = val.replace(/\D/g,'');
	if(val.length != 8) {
		return false
	}
	// Parse the date parts to integers
	var year = val.substring(0, 4);
	var month = val.substring(4, 6);
	var day = val.substring(6, 8);
	// Check the ranges of month and year
	if(year < 1000 || year > 3000 || month == 0 || month > 12) {
		return false;
	}
	var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
	// Adjust for leap years
	if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0)){monthLength[1] = 29;}
	// Check the range of the day
	return day > 0 && day <= monthLength[month - 1];
}

function isNotValidDate(val) {
	return !isValidDate(val);
}

//loaingOverlay redirect
function fnLoadingOverlayRedirect(location){
	fnLoadingShow();
	location.href = location;
}

// 검색어 엔터키 처리
function fnSearchEnter(e){
	if((e.keyCode || e.which) == 13){
		fnSearch();
		e.preventDefault();
	}
}

//주소검색
function fnJusoPop(){
	var url = "/cmmn/juso/jusoPop.do";
	window.open(url, "jusoPop", "resizable=yes, status=no, scrollbars=yes, toolbar=no, menubar=no, width=570px, height=420px");
	return false;
}

//파일다운로드
function fnFileView(idx, sn) {
	var url = "/cmmn/file/docView.do?fileIdx=" + idx + "&fileSn=" + sn;
	window.open(url, "fileView");
	return false;
}

//파일다운로드
function fnFileDownload(idx, sn) {
	var iframe = document.getElementById("hiddenFrame");
	iframe.src ="/cmmn/file/fileDownload.do?fileIdx=" + idx + "&fileSn=" + sn;
}
//콘텐츠파일 다운로드
function fnDownContentsFile(fileSaveNm, fileNm) {
	var iframe = document.getElementById("hiddenFrame");
	iframe.src ="/contents/fileDownload.do?fileSaveNm="+encodeURIComponent(fileSaveNm)+"&fileNm=" + encodeURIComponent(fileNm);
}

//업로드 허용 파일 체크
function isAllowedFile(fileName) {

	//확장자 체크
	var regExp = new RegExp("\.(php|php3|php4|asa|app|exe|cgi|phtml|html|htm|pl|asp|aspx|mdb|js|css|java|class|xml|jsp|inc|properties|com|scr|vbs|dll|cmd|sh|bat)$", "i");
	if (regExp.test(fileName) == true) {
		//alert("업로드할수 없는 확장자의 파일입니다.");
		return false;
	}
	return true;
}


function isNotAllowedFile(fileName) {
	return !isAllowedFile(fileName);
}

//loaingOverlay hide
function fnLoadingShow() {
	$.LoadingOverlay("show");
}

//loaingOverlay hide
function fnLoadingHide() {
	$.LoadingOverlay("hide", true);
}

function fnBookCheckAll(){
	if(this.checked){
		$("input[name=bookChk]").each(function(){
			$(this).prop("checked", true);
		});
	}else{
		$("input[name=bookChk]").each(function(){
			$(this).prop("checked", false);
		});
	}
}

//이미지 파일 체크
function isImageFile(fileName) {
	//확장자 체크
	var regExp = new RegExp("\.(gif|jpg|jpeg|png)$", "i");
	if (regExp.test(fileName) == false) {
		//alert("이미지파일( gif, jpg, jpeg, png)만 등록이 가능합니다.");
		return false;
	}
	return true;
}

function isNotImageFile(fileName) {
	return !isImageFile(fileName);
}

//글자수 체크
function chkword(obj, maxByte, id) {

	var strValue = obj.value;
	var strLen = strValue.length;
	var totalByte = 0;
	var len = 0;
	var oneChar = "";
	var str2 = "";

	for (var i = 0; i < strLen; i++) {
		oneChar = strValue.charAt(i);
		if (escape(oneChar).length > 4) {
			totalByte += 1;
		} else {
			totalByte++;
		}

		// 입력한 문자 길이보다 넘치면 잘라내기 위해 저장
		if (totalByte <= maxByte) {
			len = i;
		}
	}
	$("#"+id).text(totalByte + " / " + maxByte);
	// 넘어가는 글자는 자른다.
	if (totalByte > maxByte) {
		alert(maxByte + "자를 초과 입력 할 수 없습니다.");
		str2 = strValue.substr(0, len);
		obj.value = str2;
		chkword(obj, 4000);
		$("#"+id).text(maxByte + " / " + maxByte);
	}

}


//Url 인코딩
function fnEncode(unencoded) {
	return encodeURIComponent(unencoded).replace(/'/g,"%27").replace(/"/g,"%22");
}

//Url 디코딩
function fnDecode(encoded) {
	return decodeURIComponent(encoded.replace(/\+/g,  " "));
}

//화면인쇄
function printPopup(siteCd) {
	var win = window.open( "/cmmn/print/printPop.do?siteCd=" + siteCd, "popup_print", "width=763,height=500, scrollbars=yes");
	win.focus();
}

//카카오 스토리 공유하기
function fnShareKakaoStory(url) {
	Kakao.init('e7dfb65fd54a75a63129679a6a15f608');
	var postTitle = "안양시립도서관 "+$('.naviandtitle h3').text();
	Kakao.Story.share({
		url: url,
		text: postTitle
	});
}

//네이버 블로그 공유하기
function fnShareNaver(url) {
	var postTitle = "안양시립도서관 "+$('.naviandtitle h3').text();
	var shareUrl = "http://share.naver.com/web/shareView.nhn?url=" + encodeURIComponent(url) + "&title=" + encodeURI(postTitle);
	var objwin = window.open(shareUrl, 'naverSharePopup', 'width=400,height=500,scrollbars=no,menubar=0,toolbar=0');
	if (objwin) {
		objwin.focus();
	}
}

//트위터 공유하기
function fnShareTwitter(url) {
	var shareUrl = "http://twitter.com/home?status=" + encodeURIComponent("공유하기") + " " + encodeURIComponent(url);
	var objwin = window.open(shareUrl, 'twitterPopup', 'width=700,height=500,scrollbars=no,menubar=0,toolbar=0');
	if (objwin) {
		objwin.focus();
	}
}

//페이스북 공유하기
function fnShareFaceBook(url) {
	var shareUrl = "http://www.facebook.com/sharer/sharer.php?t=" + encodeURIComponent("공유하기") + "&u=" + encodeURIComponent(url);
	var objwin = window.open(shareUrl, 'facebookPopup', 'width=600,height=500,scrollbars=no,menubar=0,toolbar=0');
	if (objwin) {
		objwin.focus();
	}
}

//화면인쇄
function fnPrintPopup(siteCd) {
	var win = window.open( "/cmmn/print/printPop.do?siteCd=" + siteCd, "popup_print", "width=763,height=500, scrollbars=yes");
	win.focus();
}

//바이트계산
function fnByteLength(s) {
	var b, i, c;
	for(b=i=0;c=s.charCodeAt(i++);b+=c>>11?3:c>>7?2:1);
	return b;
}

function fnNoImgBook(img) {
	img.src = "/include/image/common/img_none.png";
}

function fnNoImgMovie(img) {
	img.src = "/include/image/common/noimg_movie.png";
}

function fnNoImgExhibition(img) {
	img.src = "/include/image/board/img_none.png";
}

function fnNoImgPhoto(img) {
	img.src = "/include/image/board/noimg_photo.png";
}

function fnNoImage(img) {
	img.src = "/include/image/common/img_none.png";
}

function dvdRregExp(str) {
	var regExp = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi
	var t = str.replace(regExp, "  ")
	var str2 = t.split('   ');
	return str2[0].trim();
}
