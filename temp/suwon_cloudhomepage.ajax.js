const GLOBAL_MESSAGE = {};
GLOBAL_MESSAGE.SERVER_ERROR_MSG     = "시스템 에러가 발생하였습니다. 지속시 관리자에게 문의하십시오.";
GLOBAL_MESSAGE.SCRIPT_ERROR_MSG     = "스크립트 에러가 발생하였습니다.<br />새로고침 후 다시 시도해 주세요.";
GLOBAL_MESSAGE.AJAX_ERROR_MSG       = "서버와의 통신중 장애가 발생하였습니다.";

const LoadingBar = {
	block : function() {
	    let loadEl = document.getElementById('loadingWrap');
		loadEl.style.display = 'block';
		if (loadEl.className.indexOf('on') < 0){
			setTimeout(function() {
		        loadEl.className = loadEl.className + 'on';
		    }, 250);
	    }
	},
	none : function() {
	    let loadEl = document.getElementById('loadingWrap');
        loadEl.className = loadEl.className.replace('on', '');
		setTimeout(function() {
            loadEl.style.display = 'none';
        }, 250);
	}
};

/**
 * @description: : AJAX 공통 호출 함수
 * @author       : JKI
 * @date         : 2022.01.25
 * @param ajaxOption
 * @param divLoadingBarId
 */
function commonAjaxRequest(ajaxOption, divLoadingBarId) {
	let option = null;
	let isBtn = false;
	let btn = null;
	const SC_UNAUTHORIZED = 401;
	let contentType = "application/x-www-form-urlencoded; charset=UTF-8";

	try {

		if ( ajaxOption.contentType ) contentType = ajaxOption.contentType;
		if ( ajaxOption.async !== false && !ajaxOption.async ) ajaxOption.async = true;
		if ( ajaxOption.btnId ) {
			isBtn = true;
			btn = $("#" + ajaxOption.btnId);
			btn.prop("disabled", true);
		}
		option = {
			url : ajaxOption.url,
			beforeSend: function(xhr, options) {
                // 임시 주석처리 차후 csrf 추가시 주석 해제
				// xhr.setRequestHeader($("meta[name='_csrf_header']").attr("content"), $("meta[name='_csrf']").attr("content"));
				xhr.setRequestHeader("ajax", true);
				if ( ajaxOption.loadingBar ) {
					if ( divLoadingBarId ) {
						divInlineLoadingBar(divLoadingBarId, "block");
					} else {
						LoadingBar.block();
					}
				}
				if(isBtn) btn.prop("disabled", true);
				$("button").prop("disabled", true);
			},
			data : ajaxOption.params,
			type : ajaxOption.method,
			async : ajaxOption.async,
			contentType : contentType,
			success : function(data) {
				if(ajaxOption.success) ajaxOption.success(data);
			},
		    error : function(response){
			    if (ajaxOption.useErrorCallback === true && ajaxOption.errorCallback ) {
		    	    ajaxOption.errorCallback(response.status);
			    } else if(response.status === SC_UNAUTHORIZED) {
		    	    if (ajaxOption.useUnAuthRedirect !== false) {
		    	        location.href = getContextPath();
                    }
		    	} else {
		    		if( ajaxOption.error ) {
	    				if (response.status === 500 || ajaxOption.useGlobalErrorMsg === false) {
	    					ajaxOption.error(response.responseJSON);
	    				} else {
	    					failAlert(GLOBAL_MESSAGE.AJAX_ERROR_MSG)
	    				}
			    	} else {
			    		failAlert(GLOBAL_MESSAGE.AJAX_ERROR_MSG);
			    	}
		    	}
		    },
		    complete : function(data) {
		    	if (ajaxOption.useCustomCompleteMethod) {
		    		ajaxOption.complete(data);
		    	}

		    	if ( ajaxOption.loadingBar ) {
					if ( divLoadingBarId ) {
						divInlineLoadingBar(divLoadingBarId, "none");
					} else {
						LoadingBar.none();
					}
				}

		    	if (window.opener && typeof window.opener.sessionExtension === "function") {
	    			opener.sessionExtension();
	    		} else if(window.sessionExtension && typeof window.sessionExtension === "function"){
	    			window.sessionExtension();
	    		}

				if(isBtn) btn.prop("disabled", false);
				$("button").prop("disabled", false);
			},
			useGlobalErrorMsg: ajaxOption.useGlobalErrorMsg
		};

		if ( ajaxOption.dataType ) option["dataType"] = ajaxOption.dataType

		$.ajax(option);

	} catch(e) {
		failAlert(GLOBAL_MESSAGE.SCRIPT_ERROR_MSG );
		console.log(e);
	}

}

var nolist_msg = "목록이 없습니다.";

function ajaxErrorMsg(response,type){
	//debug 때문에..
	if(type) {
		var err = response.status + ' ' + response.statusText;
		console.log(err);
	}
	// alert("처리 중 오류가 발생했습니다. 관리자에게 문의하세요.");
} 