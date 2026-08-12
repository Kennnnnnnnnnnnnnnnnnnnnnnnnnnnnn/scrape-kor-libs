function getContextPath() {
    return document.getElementById("ctx").value;
}

/**
 * 라벨의 텍스트를 조회
 *
 * @date 2022. 01. 25
 * @author JKI
 *
 */
function getLabelText(id) {
    return !$("label[for='" + id + "']").text()
        ? $("#" + id).prop("title")
        : $("label[for='" + id + "']").text().trim();
}

/**
 * 콤마 구분 숫자
 *
 * @date 2022. 01. 25
 * @author JKI
 *
 */
function numberWithCommas(x) {
    if(!isNaN(x) && Number(x) <= 0) return x;
    else if(x === null || x === undefined || x === '') return '';
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


/**
 * 엔터 이벤트 세팅
 *
 * @date 2022. 01. 25
 * @author JKI
 *
 */
function setEnterEvent(id, method) {

    if ({}.toString.call(method) !== '[object Function]')  {
        console.error('Invalid Function');
        return;
    }

	let targetId = getIDArrayFromString(id);
    let eventTarget = $(targetId);
    eventTarget.on("keydown", function(e){
        if ( (e.keyCode || e.which) === 13 ) {
            method();
            return false;
        }
    });
}

/**
 * 이벤트 세팅
 * @date 2022. 01. 26
 * @author JKI
 *
 * @param id
 * @param event
 * @param method
 */
function setEvent(id, event, method) {

    if ({}.toString.call(method) !== '[object Function]') {
        console.error('Invalid Function');
        return;
    }

    let targetId = getIDArrayFromString(id);
	let eventTargets = document.querySelectorAll(targetId);
	if (!eventTargets) {
		console.error('Invalid Target');
		return;
	}
	let eventFnc = function(e) {
		method(e);
	};

	for (let i = 0 ; i < eventTargets.length ; i++ ) {
		eventTargets[i].removeEventListener(event, eventFnc);
		eventTargets[i].addEventListener(event, eventFnc);
	}

}

/**
 *
 * 콤마로 구분된 스트링을 배열로 리턴하는 함수
 * @date 2022. 01. 26
 * @author JKI
 * @param ids
 */
function getIDArrayFromString(ids) {
    if (ids.indexOf(",") < 0 ) return '#' + ids;

    let splitVal = ids.replace(/ /g, "").split(",");
    let len = splitVal.length;
    let targetArr = new Array();
    for (let i = 0; i < len; i++) {
        targetArr.push('#' + splitVal[i].trim());
    }
    return ','.join(targetArr);
}

/**
 * 세션 유효시간 체크
 *
 * @date 2022. 01. 25
 * @author JKI
 *
 */
function checkSessionTime() {
	let session_minute = 0;
	let session_second = 0;
	if(session_max_time % 60 == 0) {
		session_minute = session_max_time / 60;
		session_second = 0;
	} else {
		session_minute = session_max_time / 60;
		session_second = session_max_time % 60;
	}
	
	$("#session_minute").text(Math.floor(session_minute));
	$("#session_second").text(session_second);
	
	session_max_time--;

	if(session_max_time == 0) {
		closeAlert();
		alert("장시간 미사용으로 인하여 로그아웃되었습니다.");
		goLogOut();
	} else if (session_max_time == 180) {
		sessionAlert("세션 만료 "+Math.floor(session_minute)+"분 "+session_second+"초 전 입니다.");
	}
	if (session_max_time < 180) {
		$("#sessionAlert p").text("세션 만료 "+Math.floor(session_minute)+"분 "+session_second+"초 전 입니다.");
	}
}

/**
 * @함수명 : incrementSession
 * @작업자 : CHAEUMCNI kuckjwi
 * @생성일 : 2018.08.13
 * @함수설명 : 세션 유효시간을 늘린다.
 * @변경이력 :
 */
function incrementSession() {
	if(typeof session_max_time !== 'undefined'){
		$.ajax({
			url : getContextPath() + "/common/increment/session",
			type : "get",
			success : function(data) {
				if ( parseInt(data) != -1 ) {
					session_max_time = data;
					clearInterval(session_timer);
					session_timer = setInterval("checkSessionTime()", 1000);
				} else {
					alert("세션 시간 연장에 실패하였습니다. 잠시 후 다시 시도해 주십시오.");
				}
			}
		});
	}
}

/**
 * 세션 로그아웃
 *
 * @date 2022. 01. 25
 * @author JKI
 *
 */
function goLogOut(){
	window.location.href = getContextPath() + "/logout";
}


/**
 * getBastWord : 인기검색어 조회 (임시)
 *
 * @date 2022.01.25
 * @author kjm
 * @param  manageCode : 관리 구분 , count : 조회할 숫자  (최대 10)
 * @return <li><a>#인기검색어</a></li> 형식의 문자열 
 */
function getBastWord(manageCode, count) {

	var str = "";
	
	$.ajax({
		type : 'post',
	    async: false, 
		url  : getContextPath()+'/popular/get/bestword',
        data : { "manage_code" : manageCode , "rank_count" : count},
		success : function(data){
			if(data.RESULT_INFO === "SUCCESS"){
				var rowCnt = data.LIST_DATA.length;
				if(0 < rowCnt){
					for(var i = 0; i < rowCnt; i++){
						str += "<li class='li'><a href='javascript:searchMainBook(\""+data.LIST_DATA[i].SEARCH_WORD+"\")'>#"+data.LIST_DATA[i].SEARCH_WORD+"</a></li>";
					}
				}
			}
		}
	});
	return str;
}

/**
 * numFormat : 숫자 두자리로 치환
 *
 * @date 2022.01.25
 * @author kjm
 * @param  num (숫자)
 * @return 두자리 숫자 1 => 01 
 */
function numFormat(num) {
	num = Number(num).toString();
	if(Number(num) < 10 && num.length == 1)
		num = "0" + num;
	return num; 
}

/**
 * 널값일 때 기본 문자열로 대체하는 함
 *
 * @param value
 * @param defaultStr
 * @date 2022.02.08
 * @author jki
 */
function replaceEmpty(value, defaultStr) {
	defaultStr = !defaultStr ? '-' : defaultStr;
	if(isNullCheck(value)) return defaultStr;
	return value;
}

/**
 * textLengthOverCut : 문자열 특정 길이 초과도 자르고 다른 문자로 치환
 *
 * @date 2022.02.10
 * @author kjm
 * @param  txt : 문자열 , len : 처리할 길이(기본값 20) , : lastTxt : 자른 마지막에 붙일 문자열 (기본값 ...)
 * @return txt : 일정 길이로 잘린 문자열
 */
function textLengthOverCut(txt, len, lastTxt) {
    if (isNullCheck(len)) { 
        len = 20;
    }
    if (isNullCheck(lastTxt)) {
        lastTxt = "...";
    }
    if (txt.length > len) {
        txt = txt.substr(0, len) + lastTxt;
    }
    return txt;
}

/**
 * addressQuery : 주소 조회 팝업을 Open 한다
 *
 * @date 2022.02.16
 * @author kjm
 * @param  zipcode : 우편번호 입력할 입력창 아이디 , address : 주소 입력할 입력창 아이디
 * @return
 */
function addressQuery(zipcode, address){
	let popupWindow=  window.open('', name, 'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=570, height=657' );
	popupWindow.location.href = getContextPath() + "/common/jusopopup/" + zipcode + "/" + address;
}


/**
 * jusoCallBack : 검색한 주소 정보를 항목에 입력한다.
 *
 * @date 2022.02.16
 * @author kjm
 * @param  roadFullAddr : 주소 , zipNo : 우편번호 , zipcode : 우편번호 입력할 입력창 아이디 , address : 주소 입력할 입력창 아이디
 * @return
 */
function jusoCallBack(addrID, detailAddrID, zipnoID, rtRoadFullAddr, rtAddrPart1, rtAddrDetail, rtAddrPart2, rtZipNo) {
	$("#"+zipnoID).val(rtZipNo);
	$("#"+addrID).val(rtRoadFullAddr);
}

/**
 *
 * 바이트계산 결과를 리턴
 *
 * @author JKI
 * @param limitLength
 * @param text
 */
function getByteCheck(limitLength, text){
    let strByteLenth = '';

	for(let i = 0; i < text.length; i++){
		let code = parseInt(text.charCodeAt(i));
		let ch = text.substr(i, 1).toUpperCase();

		if ((ch < "0" || ch > "9") && (ch < "A" || ch > "Z") && ((code > 255) || (code < 0))){
			strByteLenth = Number(strByteLenth) + 3; //UTF-8 3byte 로 계산
        }else{
        	strByteLenth = Number(strByteLenth) + 1;
        }
	}

	return limitLength < strByteLenth ?  true : false;
}

/**
 * 폼데이터의 직렬화
 * serialize(new FormData(data))
 * @param data
 * @returns {{}}
 */
function serialize (data) {
	let obj = {};
	for (let [key, value] of data) {
		if (obj[key] !== undefined) {
			if (!Array.isArray(obj[key])) {
				obj[key] = [obj[key]];
			}
			obj[key].push(value);
		} else {
			obj[key] = value;
		}
	}
	return obj;
}

 /**
  * replaceAll : 문자 바꾸기
  *
  * @date 2022.02.22
  * @author kjm
  * @param  sValue, param1, param2
  * @return 바뀐 문자
  */
function replaceAll(sValue, param1, param2) {
    return sValue.split(param1).join(param2);
}


/**
 * onlyNumber : 숫자 체크
 *
 * @date 2022.02.22
 * @author kjm
 * @param  
 * @return
 */
function onlyNumber(event) {
	if((event.keyCode < 48) || (event.keyCode > 57))
		return false;
}

