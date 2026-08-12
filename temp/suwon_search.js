/**
 * @description: : 자료검색 공통
 * @author       : JKI
 * @date         : 2022.01.26
 */
let kdcv = null; // 한국십진분류 로그용 변수
let kcid = null; // 카테고리분류 로그용 변수
let globalSearchParamJson = null;
let suppressCategoryAutoSearch = false;
function init() {
    const kCid = getQueryParam("kCid");
    const searchType = getQueryParam("searchType");
    const kdcValue = getQueryParam("kdcValue");
    const class_type = getQueryParam("class_type");

    if(kdcValue) {
        globalSearchKdcValue = kdcValue; // 한국십진분류
        kdcv = kdcValue;
        globalClassType = class_type;

        const kdcValueInput = document.getElementById("kdcValue");
        if (kdcValueInput) {
            kdcValueInput.value = kdcValue;
        }
    }

    if (kCid) {
        globalSearchKCID = kCid; // 카테고리분류
        kcid = kCid;

        const kCidInput = document.getElementById("kCid");
        if (kCidInput) {
            kCidInput.value = kCid;
        }
    }
    if (searchType) {
        globalSearchType = searchType;
    }
    initParam();
    initialSettings(); // 초기 화면 세팅
    getLibList(); // 도서관 목록 세팅
    setPageEvent(); // 엔터, 클릭 이벤트 세팅

    getCategoryType1(); // 카테고리 세팅 1
    setSearchType(); // 검색유형 세팅
    getPopularKeywordList(); // 인기검색어 세팅
}

function initParam() {
    if(!isNullCheck(globalSearchParam)) {
        popStateChk = true;
        if(isNullCheck(globalSearchParamJson)) {
            try {
                globalSearchParamJson = JSON.parse(globalSearchParam);
            } catch (e) {
                console.warn("SEARCH_PARAM parse error:", e);
                return;
            }
        }

        if (isNullCheck(globalSearchParamJson)) return;

        let globalSearchKind = globalSearchParamJson.searchKind;

        if(!isNullCheck(globalSearchKind)){
            $('#selectKindTab li').removeClass('on');
            $("#selectKindTab li[tab-kind="+globalSearchKind+"]").addClass('on');

            $('#bookList, #nonBookList, #eBookList, #serialList').hide();

            if (globalSearchKind === 'book') {
                $('#bookList').show();
            } else if (globalSearchKind === 'nonbook') {
                $('#nonBookList').show();
            } else if (globalSearchKind === 'ebook') {
                $('#eBookList').show();
            } else {
                $('#serialList').show();
            }
        }

        $("#isSearchType").val(globalSearchParamJson.isSearchType);
        $("#searchTxt").val(globalSearchParamJson.searchTxt);
        $("#innerSearchTxt").val(globalSearchParamJson.innerSearchTxt);
        $("#selectDisplay").val(globalSearchParamJson.displayNo);
        $("#searchTitle").val(globalSearchParamJson.searchTitle);
        $("#searchAuthor").val(globalSearchParamJson.searchAuthor);
        $("#searchPublisher").val(globalSearchParamJson.searchPublisher);
        $("#searchIsbn").val(globalSearchParamJson.searchIsbn);
        $("#searchPubYearStart").val(globalSearchParamJson.searchPubYearStart);
        $("#searchPubYearEnd").val(globalSearchParamJson.searchPubYearEnd);
        $("#searchShelf").val(globalSearchParamJson.searchShelf);
        $("#searchRegNo").val(globalSearchParamJson.searchRegNo);
        $("#searchKeyword").val(globalSearchParamJson.searchKeyword);
        $("#categoryDepth3").val(globalSearchParamJson.history_categoryDepth3);
        $("#categoryDepth2").val(globalSearchParamJson.history_categoryDepth2);
        $("#categoryDepth1").val(globalSearchParamJson.history_categoryDepth1);
        $("#kdcSection").val(globalSearchParamJson.history_kdcSection);
        $("#kdcDivision").val(globalSearchParamJson.history_kdcDivision);
        $("#kCid").val(globalSearchParamJson.kCid);
        globalSearchKCID = globalSearchParamJson.kCid;
        $("#kdc").val(globalSearchParamJson.history_kdc);
        $("#selectSort").val(globalSearchParamJson.history_selectSort);
        globalSearchKdcValue = globalSearchParamJson.kdcValue;
        $("#kdcValue").val(globalSearchParamJson.kdcValue);
        if(globalSearchParamJson.history_kdcDivision){
            globalClassType = "section";
        } else {
            globalClassType = "division";
        }

        if (globalSearchParamJson.manageCode) {
            const codes = globalSearchParamJson.manageCode.split(',');
            if ($("#isSearchType").val() === "normal") {
                showNormalTab();
                $('input[name="normalLibrary"]').each(function () {
                    const value = $(this).val();
                    if (codes.includes(value)) {
                        $(this).prop('checked', true);
                    } else {
                        $(this).prop('checked', false);
                    }
                });
            } else {
                showDetailTab();
                $('input[name="detailLibrary"]').each(function () {
                    const value = $(this).val();
                    if (codes.includes(value)) {
                        $(this).prop('checked', true);
                    } else {
                        $(this).prop('checked', false);
                    }
                });
            }
        }
    }
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function setCategoryVisibility({ depth1 = true, depth2 = false, depth3 = false }) {

    if (depth1) { $("#categoryDepth1").show(); } else { $("#categoryDepth1").val("").hide(); }
    if (depth2) { $("#categoryDepth2").show(); } else { $("#categoryDepth2").val("").empty().hide(); }
    if (depth3) { $("#categoryDepth3").show(); } else { $("#categoryDepth3").val("").empty().hide(); }
}
function applyVisibilityByMaxDepth() {
    if (presetMaxDepth === 1) {
        setCategoryVisibility({ depth1: true, depth2: false, depth3: false });
    } else if (presetMaxDepth === 2) {
        setCategoryVisibility({ depth1: true, depth2: true, depth3: false });
    } else if (presetMaxDepth === 3) {
        setCategoryVisibility({ depth1: true, depth2: true, depth3: true });
    }
}
function getCategoryType1(){
    let makeHtml = "<option value=''>전체</option>"
    commonAjaxRequest({
        method : 'GET',
        url  : getContextPath()+'/category/get/depth1',
        params : {
        },
        success : function(data){
            $("#categoryDepth1").empty();

            for(let i = 0; i < data.depth1_result.length; i++) {
                let category = data.depth1_result[i];
                makeHtml += "<option value='" + category.DEPTH1_ID + "'>" + category.DEPTH1 + "</option>";
            }

            $("#categoryDepth1").append(makeHtml);

            setCategoryVisibility({ depth1: true, depth2: false, depth3: false });
        },
        error:function(err){
            if (err) {
                console.error(err);
            }
        },
    })
}

function getCategoryType2(depth1Id, opts){
    const maxDepth = opts?.maxDepth ?? 3; // 기본은 3
    if (!depth1Id) { setCategoryVisibility({ depth1:true, depth2:false, depth3:false }); return; }

    let makeHtml = "<option value=''>전체</option>";
    commonAjaxRequest({
        method : 'GET',
        url  : getContextPath()+'/category/get/depth2',
        params : { depth1Id },
        success : function(data){
            $("#categoryDepth2").empty();
            for (const c of data.depth2_result) {
                makeHtml += "<option value='" + c.DEPTH2_ID + "'>" + c.DEPTH2 + "</option>";
            }
            $("#categoryDepth2").append(makeHtml);

            // 매 호출마다 이번 요청의 maxDepth로 가시성 고정
            if (maxDepth === 1) setCategoryVisibility({ depth1:true, depth2:false, depth3:false });
            else                setCategoryVisibility({ depth1:true, depth2:true,  depth3:false });

            if (depthValue.active) {
                $("#categoryDepth1").val(depth1Id);

                if (depthValue.d2) {
                    $("#categoryDepth2").val(depthValue.d2);
                    getCategoryType3(depthValue.d2, { maxDepth });
                } else {
                    if (searchYN) { // 자동검색방지
                        searchYN = false;
                        depthValue = { d2: null, d3: null, active: false };

                        if (globalSearchHistoryChk != "Y") {
                            searchData(true);
                        }
                    }
                }
            }
        },
        error:function(err){ if (err) console.error(err); },
    });
}

function getCategoryType3(depth2Id, opts){
    const maxDepth = opts?.maxDepth ?? 3; // 기본은 3
    if (!depth2Id) {
        // D2가 비어 있으면 D3는 숨김
        setCategoryVisibility({ depth1:true, depth2:true, depth3:false });
        return;
    }

    let makeHtml = "<option value=''>전체</option>";
    commonAjaxRequest({
        method : 'GET',
        url  : getContextPath()+'/category/get/depth3',
        params : { depth2Id },
        success : function(data){
            $("#categoryDepth3").empty();
            for (const c of data.depth3_result) {
                makeHtml += "<option value='" + c.DEPTH3_ID + "'>" + c.DEPTH3 + "</option>";
            }
            $("#categoryDepth3").append(makeHtml);

            if (maxDepth === 3) setCategoryVisibility({ depth1:true, depth2:true, depth3:true });
            else                setCategoryVisibility({ depth1:true, depth2:true, depth3:false });

            if (depthValue.active && depthValue.d3) {
                $("#categoryDepth3").val(depthValue.d3);
            }

            if (searchYN) {
                searchYN = false;
                depthValue = { d2: null, d3: null, active: false };

                if (globalSearchHistoryChk != "Y") {
                    searchData(true);
                }
            }
        },
        error:function(err){ if (err) console.error(err); },
    });
}

/**
 * 검색유형이 있을 경우에 대한 세팅 처리
 */
function setSearchType() {
    if ('detail' === globalSearchType) {
        showDetailTab();
    }
}

function htmlDecode(str) {
    const txt = document.createElement('div');
    txt.innerHTML = decodeURIComponent(str);
    return txt.textContent || txt.innerText || '';
}

/**
 * 파라미터가 있는 인자에 대한 세팅
 */
function setSearchCallParams() {

    let categoryFunctionLog = "카레고리분류검색";
    let kdcFunctionLog = "한국십진분류검색";

    let checkLIb = !globalSearchLib ? null : $("#normalLib_"+globalSearchLib);
    if (checkLIb) {
        checkLIb.prop("checked", true);
    } else {
        const libraryId = getSearchType() === 'normal' ? 'normalLibraries' : 'detailLibraries';
        let els = document.querySelectorAll('#'+libraryId+' input[type=checkbox]');
        for (let i = 0 ; i < els.length ; i++ ) {
            els[i].checked = true;
        }
    }
    if(globalSearchWords) {
        let decodedWord = htmlDecode(globalSearchWords);
        document.getElementById('searchTxt').value = decodedWord;
    }
    if (globalSearchKdcValue != null && globalSearchKdcValue != "") {
        suppressCategoryAutoSearch = true; // 자동검색방지
        $("#searchKdcCode").val(globalSearchKdcValue);

        const v1 = globalSearchKdcValue.substring(0, 1);
        const v2 = globalSearchKdcValue.substring(0, 2) + "0";
        const v3 = globalSearchKdcValue;

        $("#kdc").val(v1);

        // 2뎁스 설정
        getKDCList($("#kdc").val(), 'select', 'division', function () {
            $("#kdcDivision").val(v2);  // 2뎁스 셀렉트박스 보여주기
        });

        getKDCList($("#kdc").val(), 'select', 'division', function () {
            $("#kdcDivision").val(v2).show();
            if (globalClassType === "section") {
                getKDCList($("#kdcDivision").val(), 'select', 'section', function () {
                    $("#kdcSection").val(v3).show();
                });
            } else {
                $("#kdcSection").hide().empty();
            }
        });
    }
    if(globalSearchKCID != null && globalSearchKCID != "") {
        const len = globalSearchKCID.length;
        const depth1 = globalSearchKCID.substring(0, 3);
        const depth2 = globalSearchKCID.substring(0, 6);
        const depth3 = globalSearchKCID.substring(0, 9);
        const maxDepth = (len >= 9) ? 3 : (len >= 6) ? 2 : 1;

        if (maxDepth === 3) {
            depthValue = { d2: depth2, d3: depth3, active: true };
            searchYN = true;
            getCategoryType2(depth1, { maxDepth });

        } else if (maxDepth === 2) {
            depthValue = { d2: depth2, d3: null, active: true };
            searchYN = true;
            getCategoryType2(depth1, { maxDepth });

        } else { // maxDepth === 1
            depthValue = { d2: null, d3: null, active: true };
            searchYN = true;
            getCategoryType2(depth1, { maxDepth });
        }
    }
    if(globalSearchHistoryChk != "Y" && !searchYN) {
        searchData(true);
    } else if(globalSearchHistoryChk == "Y") {
        search(true, false, globalSearchParamJson);
        globalSearchParamJson= null;
    }
    // 초기화
    globalSearchWords = '';
    globalSearchLib = '';
    globalSearchType = '';
    globalSearchKCID = '';
    globalSearchKdcValue = '';
    globalIsSearchType = '';
    globalSearchParam = '';
}


/**
 * initUrlManageCode : url 메니지코드 있는경우 기본 url 도서관으로 체크 하도록 처리
 *
 * @date 2022.01.25
 * @author kjm
 * @param
 * @return
 */
function initUrlManageCode() {
    if(!isNullCheck(defUrlManageCode)){
        //노말검색
        document.querySelector('#normalLibraries input[type=checkbox][value='+ defUrlManageCode +']').checked = true;

        //상세검색
        document.querySelector('#detailLibraries input[type=checkbox][value='+ defUrlManageCode +']').checked = true;
    } else {
        //노말검색
        $('#normalLibraries input[type=checkbox]').prop('checked',true);

        //상세검색
        $('#detailLibraries input[type=checkbox]').prop('checked',true);
    }
}


/**
 * 패싯 데이터 객체
 */
let GLOBAL_FACETS = {
    facetLib : '',
    facetLibName : '',
    facetAuthor : '',
    facetPublisher : '',
    facetPubYear : '',
    facetSubject : '',
    facetSubjectName : '',
    facetMedia : '',
    facetMediaName : ''
}

/**
 * 패싯 초기화
 */
function resetGlobalFacet() {
    GLOBAL_FACETS = {
        facetLib: '',
        facetLibName: '',
        facetAuthor: '',
        facetPublisher: '',
        facetPubYear: '',
        facetSubject: '',
        facetSubjectName: '',
        facetMedia: '',
        facetMediaName: ''
    }
}

/**
 * 이벤트 세팅
 */
function setPageEvent() {

    // enter event
    setEnterEvent('searchTxt', function(){searchData(true);});
    setEnterEvent('innerSearchTxt', innerSearch);

    setEnterEvent('searchTitle', function(){searchData(true);});
    setEnterEvent('searchAuthor', function(){searchData(true);});
    setEnterEvent('searchPublisher', function(){searchData(true);});
    setEnterEvent('searchIsbn', function(){searchData(true);});
    setEnterEvent('searchPubYearStart', function(){searchData(true);});
    setEnterEvent('searchPubYearEnd', function(){searchData(true);});
    setEnterEvent('searchShelf', function(){searchData(true);});
    setEnterEvent('searchRegNo', function(){searchData(true);});
    setEnterEvent('searchKeyword', function(){searchData(true);});

    // click event
    setEvent("normalSearchBtn", "click", function(){searchData(true);});
    setEvent("detailSearchBtn", "click", function(){searchData(true);});
    setEvent("innerSearchBtn", "click", innerSearch);

    // 자료검색 페이지 이동시 기본값으로 이력 설정
    let normalSearchMenu1 = "자료검색";
    let normalSearchMenu2 = "일반검색";
    //insertMenuLog(normalSearchMenu1, normalSearchMenu2);
    
    setEvent('normalBtn', 'click', showNormalTab);
    setEvent('detailBtn', 'click', showDetailTab);
    setEvent('refreshBtn', 'click', refreshPage);

    $('#selectKindTab li').on('click', function (evt) {
        searchKindData(evt);
    });

    setEvent('openLibList', 'click', function() {openLibList("nomal");});
    setEvent('closeLibList', 'click', function() {closeLibList("nomal");});

    setEvent('openDetailLibList', 'click', function() {openLibList("detail");});
    setEvent('closeDetailLibList', 'click', function() {closeLibList("detail");});
}

/**
 * 초기화
 */
function refreshPage() {

    let form = document.createElement('form');
    form.setAttribute('id', 'refreshForm');
    form.setAttribute('method', 'post');
    form.setAttribute('action', getContextPath() + '/search');

    let hidden = document.createElement('input');
    hidden.setAttribute('type', 'hidden');
    hidden.setAttribute('name', 'searchType');
    hidden.setAttribute('value', 'detail');
    form.appendChild(hidden);

    document.body.appendChild(form);
    form.submit();
    document.getElementById('refreshForm').remove();

}
/**
 * kdc 한국십진분류 조회
 */
function getKDCList(classCode, type, selectType, done) {
    const  $division = $("#kdcDivision");
    const  $section = $("#kdcSection");

    if (!classCode) {
        $division.empty().hide();
        $section.empty().hide();
        return;
    }
    commonAjaxRequest({
        method: 'get',
        url: getContextPath() + '/get/kdc',
        params: {
            resultType: type,
            class_no: classCode,
            class_type: selectType
        },
        success: function(data) {
            if (selectType === "division") {
                $section.empty().hide();
                $division.show().empty().html(data.select);

            } else if (selectType === "section") {
                $section.show().empty().html(data.select);

            }
            if (typeof done === "function") done();

        },
        error: function(response) {
            console.error(response);
        },
        loadingBar: false
    });
}

/**
 * 검색 대상 도서관 목록 조회
 */
function getLibList() {
    commonAjaxRequest({
        method : 'get',
        url  : getContextPath() + '/getLibInfoList',
        success : function(data){
            if (!data || !data.LIB_LIST || 1 > data.LIB_LIST.length ) {
                return;
            }

            setLibList(data);
            if (globalSearchWords || globalSearchKCID || globalSearchKdcValue || globalSearchParamJson) {
                setSearchCallParams();
            } else {
                initUrlManageCode();
            }
        },
        error:function(response){
            console.error(response);
        },
        loadingBar : false
    });
}

/**
 * 인기검색어 목록 생성
 */
function getPopularKeywordList() {

    commonAjaxRequest({
        method : 'get',
        url  : getContextPath()+'/popular/get/bestword',
        params : { "manage_code" : globalManageCode , "rank_count" : 10},
        success : function(data){

            let popularEl = document.getElementById('searchPopular');
            popularEl.innerHTML = '';
            let htmlArr = [];

            if(data && data.RESULT_INFO === "SUCCESS" && data.LIST_DATA && 0 < data.LIST_DATA.length){

                popularEl.innerHTML = '<dt>인기검색어</dt>';
                popularEl.style.display = '';
                const rowCnt = data.LIST_DATA.length;

                for( let i = 0; i < rowCnt; i++){
                    const popData = data.LIST_DATA[i];
                    htmlArr.push('<dd><a href="javascript:searchKeyword(\''+popData.SEARCH_WORD+'\')">');
                    htmlArr.push('#'+popData.SEARCH_WORD);
                    htmlArr.push('</a></dd>');
                }

                popularEl.innerHTML += htmlArr.join('');
            }
        }
    });
}

/**
 * 도서관 선택 접기 및 펼치기 이벤트
 */
function setLibList(data) {
    let selectLibEl = document.querySelector('#normalLibraries > ul');
    let lis = selectLibEl.querySelectorAll('li');
    for (let i = 0 ; i < lis.length ; i++ ) {
        if (!lis[i].querySelector('#normalLib_ALL')) lis[i].remove();
    }

    for (let i = 0 ; i < data.LIB_LIST.length ; i++ ) {
        let d = data.LIB_LIST[i];
        let html = '<li><input type="checkbox" name="normalLibrary" value="'+d.manage_code+'" id="normalLib_'+d.manage_code+'"/>';
        html += '<label for="normalLib_'+d.manage_code+'">'+d.nickname+'</label></li>';
        selectLibEl.innerHTML += html;
    }

    selectLibEl = document.querySelector('#detailLibraries');
    lis = selectLibEl.querySelectorAll('li');
    for (let i = 0 ; i < lis.length ; i++ ) {
        if (!lis[i].querySelector('#detailLib_ALL')) lis[i].remove();
    }


    for (let i = 0 ; i < data.LIB_LIST.length ; i++ ) {
        let d = data.LIB_LIST[i];
        let html = '<li><input type="checkbox" name="detailLibrary" value="'+d.manage_code+'" id="detailLib_'+d.manage_code+'"/>';
        html += '<label for="detailLib_'+d.manage_code+'">'+d.nickname+'</label></li>';
        selectLibEl.innerHTML += html;
    }

    // set checkbox event
    setCheckBoxEvent();

}

/**
 * 체크박스 이벤트 추가
 */
function setCheckBoxEvent() {
    // select all
    setEvent('normalLib_ALL', 'click', function(evt) { selectLibAll(evt, 'NORMAL')});
    setEvent('detailLib_ALL', 'click', function(evt) { selectLibAll(evt, 'DETAIL')});
}

/**
 *  전체선택 이벤트 처리
 */
function selectLibAll(evt, type) {
    let target = evt.target;
    let libraryId = 'DETAIL' === type ? 'detailLibraries' : 'normalLibraries';
    let libraryEl = document.getElementById(libraryId);
    let els = libraryEl.querySelectorAll('input[type=checkbox]:not([value="ALL"])');
    for (let i = 0 ; i < els.length ; i++ ) {
        els[i].checked = target.checked ? true : false;
    }
}

/**
 * 초기 화면 세팅팅
 *
 */
function initialSettings() {
    // 검색 결과 화면 초기화
    showSearchContent(false);
}

/**
 * 검색 결과 화면을 세팅
 * @param doShow
 */
function showSearchContent(doShow) {

    let searchContent = document.getElementsByClassName('searchContent')[0];
    searchContent.className = searchContent.className.replace('hidden', '').replace(' ', '');
    if (!doShow) {
        searchContent.className += ' hidden';
    }
}

/**
 * 상세 검색 조건 show/hide
 * @param
 */
function showDetailSearchOpt() {

    commonAjaxRequest({
        method : 'post',
        url  : getContextPath() + '/search/get/detali/opt',
        success : function(data){
//        	if(data.libYN == "N"){
//        		$("#searchLibTr").hide();
//        	} else {
//        		$("#searchLibTr").show();
//        	}
//        	if(data.titleYN == "N"){
//            	$("#searchTitleTr").hide();
//        	} else {
//            	$("#searchTitleTr").show();
//        	}
            if(data.authorYN == "N"){
                $("#searchAuthorTr").hide();
            } else {
                $("#searchAuthorTr").show();
            }
            if(data.publisherYN == "N"){
                $("#searchPublisherTr").hide();
            } else {
                $("#searchPublisherTr").show();
            }
            if(data.isbnYN == "N"){
                $("#searchIsbnTr").hide();
            } else {
                $("#searchIsbnTr").show();
            }
            if(data.pubyearYN == "N"){
                $("#searchPubYearStartTr").hide();
            } else {
                $("#searchPubYearStartTr").show();
            }
            if(data.shelfYN == "N"){
                $("#searchShelfTr").hide();
            } else {
                $("#searchShelfTr").show();
            }
            if(data.regnoYN == "N"){
                $("#searchRegNoTr").hide();
            } else {
                $("#searchRegNoTr").show();
            }
            if(data.keywordYN == "N"){
                $("#searchKeywordTr").hide();
            } else {
                $("#searchKeywordTr").show();
            }
        },
        error:function(response){
            console.error(response);
        },
        loadingBar : false
    });
}

/**
 * 일반검색 탭으로 이동
 */
function showNormalTab() {
    let normalSearchMenu1 = "자료검색";
    let normalSearchMenu2 = "일반검색";
    insertMenuLog(normalSearchMenu1, normalSearchMenu2);
    changeTab('normal');
}

/**
 * 상세검색 탭으로 이동
 */
function showDetailTab() {
    let detailSearchMenu1 = "자료검색";
    let detailSearchMenu2 = "상세검색";
    insertMenuLog(detailSearchMenu1, detailSearchMenu2);
    changeTab('detail');
}

/**
 * 탭이동
 * @param evt
 */
function changeTab(show) {

    let n = document.getElementById('normalBtn').parentNode;
    let d = document.getElementById('detailBtn').parentNode;

    let normalSearch = document.getElementById('normalSearch');
    let detailSearch = document.getElementById('detailSearch');
    if ('normal' === show ) { // 클릭한게 일반검색일때
        if (n.className.indexOf('on') < 0) {
            n.className += ' on';
            d.className = d.className.replace('on', '').replace(' ', '');
        }

        // show normal, hide detail
        normalSearch.style.display = '';
        detailSearch.style.display = 'none';

    } else { // 클릭한게 상세검색일때
        if (d.className.indexOf('on') < 0) {
            d.className += ' on';
            n.className = n.className.replace('on', '').replace(' ', '');
        }

        // show detail, hide normal
        normalSearch.style.display = 'none';
        detailSearch.style.display = '';

        showDetailSearchOpt();
    }
}

/**
 * 도서, 비도서, 연속 검색
 * @param evt
 */
function searchKindData(evt) {
    evt.preventDefault();
    const $target = $(evt.currentTarget); // li가 클릭된걸로 처리
    //const $target = $(evt.target).closest('li');
    $('#selectKindTab .on').removeClass('on');

    $target.addClass('on');

    createNoResult(true);

    const tabKind = $target.attr('tab-kind');

    $('#bookList, #nonBookList, #eBookList, #serialList').hide();

    if (tabKind === 'book') {
        $('#bookList').show();
    } else if (tabKind === 'nonbook') {
        $('#nonBookList').show();
    } else if (tabKind === 'ebook') {
        $('#eBookList').show();
    } else {
        $('#serialList').show();
    }

    searchData(true);
}
/**
 * 검색 이벤트 처리
 * @param isSearch
 */
function searchData(isSearch) {
    // 결과내 검색어 초기화
    document.getElementById('innerSearchTxt').value = '';
    $("#isInnerChk").val(false);
    const type = getSearchType();
    if ( type === 'normal' ) {

        const searchTxt = document.getElementById('searchTxt').value;

        if (!searchTxt || 0 > searchTxt.replaceAll(' ', '').length) {
            alert('검색어를 입력해주세요.');
            return;
        }
        
        $("#isSearchType").val("normal");
    } else {
        const searchOptions = [ 'searchTitle', 'searchAuthor', 'searchPublisher',
            'searchIsbn', 'searchPubYearStart', 'searchPubYearEnd', 'searchShelf', 'searchRegNo', 'searchKeyword',
            'kdc','kdcDivision','kdcSection',
            'categoryDepth1','categoryDepth2','categoryDepth3', 'kCid', 'kdcValue'];

        let isValid = false;
        for (let i = 0 ; i < searchOptions.length ; i++ ) {
            let searchTxt = document.getElementById(searchOptions[i]).value;
            if (searchTxt && 0 <  searchTxt.replaceAll(' ', '').length) {
                isValid = true;
            }
        }

        if(!isValid) {
            alert('검색어를 입력해주세요.');
            return;
        }
        $("#isSearchType").val("detail");
    }

    // 패싯 초기화
    resetGlobalFacet();

    search(false, isSearch);
}

/**
 * 결과내검색
 */

function innerSearch(evt) {

    const searchTxtObj = document.querySelector('#innerSearchTxt');
    const searchTxt = searchTxtObj.value.trim();

    if (!searchTxt) {
        alert('결과 내 검색어를 입력해주세요.');
        return false;
    }
    $("#isInnerChk").val(true);

    // 패싯 초기화
    resetGlobalFacet();

    search(true, true);
}

/**
 * 결과내검색
 */
function innerSearchPage(evt) {
    const searchTxtObj = document.querySelector('#innerSearchTxt');
    const searchTxt = searchTxtObj.value;
    if (!searchTxt) {
        warningAlert('결과 내 검색어를 입력해주세요.');
        return;
    }
    $("#isInnerChk").val(true);

    // 패싯 초기화
    resetGlobalFacet();

    search(true, false);
}

/**
 * 검색 유형 체크 NORMAL, DETAIL
 * @returns {string}
 */
function getSearchType() {
    if(!isNullCheck(globalIsSearchType)){
        return globalIsSearchType;
    } else {
        const typeEl = document.querySelector('#selectTypeTab > .on');
        return typeEl.getAttribute('tab-type') ? typeEl.getAttribute('tab-type') : 'normal';
    }
}

/**
 * 검색 종류 체크
 * BOOK, NONBOOK, SERIAL
 */
function getSearchKind() {
    const kindEl = document.querySelector('#selectKindTab > .on');

    // kindEl이 존재하지 않으면 기본값 'book' 반환
    if (!kindEl) return 'book';

    const tabKind = kindEl.getAttribute('tab-kind');
    return tabKind ? tabKind : 'book';
}

/**
 * 선택된 도서관 목록을 문자열로 반환
 */
function getCheckedLibrary() {
    const name = 'normal' === getSearchType() ? 'normalLibrary': 'detailLibrary';
    const checkedLibraries = document.querySelectorAll('input[name='+name+']:checked');

    let libArr = new Array();
    for (let i = 0 ; i < checkedLibraries.length ; i++ ) {
        let checkedVal = checkedLibraries[i].value;
        if (checkedVal === 'ALL') continue;
        libArr.push(checkedVal);
    }

    if (libArr.length < 1 && globalManageCode ) {
        const libraryEl = document.querySelector('input[name='+name+'][value='+globalManageCode+']');
        if (libraryEl) {
            libraryEl.checked = true;
            libArr.push(globalManageCode);
        }
    }

    if (libArr.length < 1) {
        const libraries = document.querySelectorAll('input[name='+name+']');
        for (let i = 0 ; i < libraries.length ; i++ ) {
            if (libraries[i].value === 'ALL') continue;
            libArr.push(libraries[i].value);
        }
    }

    return libArr.join(',');
}


/**
 * 검색 인자값 세팅
 * @param type
 * @param isInner
 * @returns {{isInnerSearch: (string), searchKind: (string|string)}}
 */
function getSearchParam(type, isInner) {
    //let kCid = globalSearchKCID;
    let kCid = null;
    let kdcValue = null;
    const commonsObj = {
        searchKind : getSearchKind(),
        manageCode : getCheckedLibrary(),
        isInnerSearch: isInner ? 'T' : 'F',
        innerSearchTxt : document.getElementById('innerSearchTxt').value,
        keywordSearch: false,
        displayNo : document.getElementById('selectDisplay').value,
        orderbyItem : getOrderbyItem(),
        orderby : getOrderBy(),
        pageNo : document.getElementById('pageno').value,
    }
    if ('detail' === type) {

        // ------- 카테고리분류 -------
        // 3뎁스가 선택되었으면 3뎁스 값을 사용
        if (document.getElementById('categoryDepth3').value.trim() !== "") {
            kCid = document.getElementById('categoryDepth3').value;
        }
        // 3뎁스가 선택되지 않았으면 2뎁스 값을 사용
        else if (document.getElementById('categoryDepth2').value.trim() !== "") {
            kCid = document.getElementById('categoryDepth2').value;
        }
        // 2뎁스도 선택되지 않았으면 1뎁스 값을 사용
        else if (document.getElementById('categoryDepth1').value.trim() !== "") {
            kCid = document.getElementById('categoryDepth1').value;
        }
        // --------------------------
        
        // ------- 한국십진분류 -------

        if (globalSearchKdcValue && globalSearchKdcValue.trim() !== "") {
            kdcValue = globalSearchKdcValue;
        } else {
            if (document.getElementById('kdcSection').value) { // section
                kdcValue = document.getElementById('kdcSection').value;
            } else if (document.getElementById('kdcDivision').value) { // 전체일때
                kdcValue = document.getElementById('kdcDivision').value;
            } else {
                kdcValue = document.getElementById('kdc').value;
            }
        }
        // --------------------------

        return Object.assign({}, {
            searchTitle: document.getElementById('searchTitle').value,
            searchAuthor: document.getElementById('searchAuthor').value,
            searchPublisher: document.getElementById('searchPublisher').value,
            searchIsbn: document.getElementById('searchIsbn').value,
            searchPubYearStart: document.getElementById('searchPubYearStart').value,
            searchPubYearEnd: document.getElementById('searchPubYearEnd').value,
            searchShelf: document.getElementById('searchShelf').value,
            searchRegNo: document.getElementById('searchRegNo').value,
            searchKeyword: document.getElementById('searchKeyword').value,
            history_categoryDepth3: document.getElementById('categoryDepth3').value,
            history_categoryDepth2: document.getElementById('categoryDepth2').value,
            history_categoryDepth1: document.getElementById('categoryDepth1').value,
            history_kdcSection: document.getElementById('kdcSection').value,
            history_kdcDivision: document.getElementById('kdcDivision').value,
            history_kdc: document.getElementById('kdc').value,
            history_selectSort:document.getElementById("selectSort").value,
            kCid: kCid,
            kdcValue : kdcValue
        }, commonsObj, GLOBAL_FACETS);
    } else {
        return Object.assign({}, {
            searchTxt : document.getElementById('searchTxt').value,
            kCid: "",
            kdcValue: ""
        }, commonsObj, GLOBAL_FACETS);
    }
}

function getOrderbyItem() {
    const orderbyItem = document.getElementById('selectSort').value;
    if ("0" === orderbyItem ) return "ACCURACY_SORT";
    if ("1" === orderbyItem ) return "PUB_YEAR_INFO";
    if ("2" === orderbyItem ) return "TITLE_INFO_SORT";

    return "TITLE_INFO_SORT";
}

function getOrderBy() {
    const orderbyItem = document.getElementById('selectSort').value;
    if ("0" === orderbyItem ) return "DESC"; // ACCURACY_SORT
    if ("1" === orderbyItem ) return "DESC"; // PUB_YEAR_INFO
    if ("2" === orderbyItem ) return "ASC";  // TITLE_INFO_SORT

    return "ASC";
}

/**
 * 검색 요청
 * @param paging 페이징
 * @param isInner 결과내 검색인지 여부
 */
function search(isInner, isSearch, historyParams) {
    showSearchContent(true);
    let params;
    const type = !isNullCheck($("#isSearchType").val()) ? $("#isSearchType").val() : getSearchType();

    if(!isNullCheck(historyParams)){
        params = historyParams;
        $("#pageno").val(historyParams.pageNo);
    } else if (isSearch) {
        $("#pageno").val("1");
        params = getSearchParam(type, isInner);
    } else {
        params = getSearchParam(type, isInner);
    }



    commonAjaxRequest({
        method: 'post',
        url: getContextPath() + '/getSearchResult/' + type,
        params: params,
        success: function(data) {

            setSearchMetaInfo(data.SEARCH_RESULT, data.SEARCH_PARAMS);
            updateCountElements(data.SEARCH_COUNTS);

            if (!data.SEARCH_RESULT || (data.SEARCH_RESULT.SEARCH_COUNT || 0) < 1) {
                setNoDataList();
                return;
            }
            setSearchResult(data.SEARCH_RESULT, data.SEARCH_PARAMS, data.USER_NO, data.USER_CLASS_CODE);

            if (isNullCheck(historyParams)) {
                const query = $.param(params);
                const url = getContextPath() + '/search?historyChk=Y&isSearchType='+type + (query ? ('&' + query) : '');
                history.pushState('', '', url);
            }
        },
        error: function(err) {
            console.error(err || "Unknown error");
            setSearchMetaInfo(null, params);
            setNoDataList();
            updateCountElements({});
        },
        loadingBar: true
    });
}

function updateCountElements(counts) {
    $("#bookCnt").empty().html("(" + (counts.bookCnt || 0) + ")");
    $("#serialCnt").empty().html("(" + (counts.serialCnt || 0) + ")");
    $("#nonbookCnt").empty().html("(" + (counts.nonbookCnt || 0) + ")");
    $("#ebookCnt").empty().html("(" + (counts.ebookCnt || 0) + ")");
}


/**
 * 팝업 닫힐때 재검색
 */
function popCloseSearch(){
    search(($("#isInnerChk").val() == "true") ? true : false, false);
}

/**
 * 검색결과 세팅
 */
function setSearchResult(searchResult, searchParams, userNo, userClassCode) {
    // 검색 결과 목록
    if (searchResult.SEARCH_LIST && 0 < searchResult.SEARCH_LIST.length ) {

        // 패싯 세팅
        createFacetElements(searchResult.FACET_GROUP, searchParams);

        // 검색 목록 없음 제거
        removeNoResult();

        // 검색 본문 세팅
        createContentElements(searchResult.SEARCH_LIST, userNo, userClassCode);
        const l = document.getElementById('facetDiv').querySelector('.limits');
        
        // 모바일 화면일때 검색후 도서관목록 닫히도록 설정
        if (window.innerWidth <= 768) {
            const normalLibDiv = document.getElementById('normalLibraries');
            if (normalLibDiv) {
                // 1. 클래스 변경
                normalLibDiv.classList.remove('open');
                normalLibDiv.classList.add('close');

                // 2. 버튼 표시 전환
                const openBtn = document.getElementById('openLibList');
                const closeBtn = document.getElementById('closeLibList');

                if (openBtn) openBtn.classList.remove('hidden'); // 펼치기 버튼 보이기
                if (closeBtn) closeBtn.classList.add('hidden');   // 닫기 버튼 숨기기
            }
        }

        if(l) {
            // paging

            new CSPaging('paging', 'selectDisplay', 'pageno', searchFacetPage, searchResult.SEARCH_COUNT).init();
        } else {
            if (kdcv) {
                insertFunctionLog("한국십진분류검색");
                kdcv = "";
            } else if (kcid) {
                insertFunctionLog("카테고리분류검색");
                kcid = "";
            } else {
                insertFunctionLog("검색");
            }
            // paging
            new CSPaging('paging', 'selectDisplay', 'pageno', ($("#isInnerChk").val() == "true") ? innerSearchPage : searchData, searchResult.SEARCH_COUNT).init();
        }
        window.scrollTo({ top: 300, behavior: 'smooth' });

    } else {
        // 결과 없음 세팅
        setNoDataList();
    }


}

/**
 * 검색결과없음 메세지 제거
 */
function removeNoResult() {
    createNoResult(false);
}

/**
 * 검색 결과없음 메세지 셍성
 * @param doCreate t
 */
function createNoResult(doCreate) {
    let noResultEl = document.getElementById('noResultDiv');

    if (doCreate) {
        document.getElementById('bookList').innerHTML = '';
        document.getElementById('nonBookList').innerHTML = '';
        document.getElementById('serialList').innerHTML = '';
        document.getElementById('eBookList').innerHTML = '';

        if (!noResultEl) {
            document.getElementById('searchResultDiv').innerHTML += '<div class="search_no_result" id="noResultDiv"><p>검색된 도서내역이 없습니다.</p></div>';
        }

    } else {
        if(noResultEl) noResultEl.remove();
    }

}


/**
 * 검색결과없음 세팅
 */
function setNoDataList() {


    // remove facet
    removeFacetElement();

    // hide inner search ...??
    // hide paging
    document.getElementById('paging').innerHTML = '';
    document.getElementById('pageno').value = 1;

    // set no data content
    createNoResult(true);
}

/**
 * 검색 메타 정보 세팅
 * @param searchCount
 * @param searchParams
 */
function setSearchMetaInfo(searchResult, searchParams) {

    // 검색어에 대한 세팅
    let metaInfo = document.getElementById('searchMeta');
    if (!searchParams) {
        metaInfo.innerHTML = '';
        return;
    }

    let count =  (!searchResult || 1 > searchResult.SEARCH_COUNT) ? 0 : searchResult.SEARCH_COUNT;

    let metaArr = new Array();
    if ('normal' === getSearchType()) {
        metaArr.push('<strong>"');
        metaArr.push(searchParams.searchTxt);
        metaArr.push('"</strong>에 대하여 ');
    }

    metaArr.push('전체 <span>');
    metaArr.push(count);
    metaArr.push('</span>개가 검색되었습니다.');
    metaInfo.innerHTML = metaArr.join('');
}

/**
 * 패싯 결과 초기화
 */
function removeFacetElement() {
    createFacetElements();
}

/**
 * 패싯 목록 세팅
 * @param facetList
 */
function createFacetElements(facetList, searchParams) {

    // 기존 제한 패싯 초기화
    const l = document.getElementById('facetDiv').querySelector('.limits');
    if(l) {
        l.remove();
    }


    let isEmptyList = facetList ? false : true;
    let facetHtml = document.getElementById('template-facet-item').innerHTML;

    // 도서관 패싯 세팅
    let hasLibGroup = !isEmptyList && (facetList.LIB_GROUP && 0 < facetList.LIB_GROUP.length);
    facetHtml = facetHtml.replace('{LIB_FACET_DATA}', hasLibGroup ? createFacetListHtml( facetList.LIB_GROUP, 'NAME', 'facetLib') : '');

    // 저자 패싯 세팅
    let hasAuthorGroup = !isEmptyList && (facetList.AUTHOR_GROUP && 0 < facetList.AUTHOR_GROUP.length);
    facetHtml = facetHtml.replace('{AUTHOR_FACET_DATA}', hasAuthorGroup ? createFacetListHtml( facetList.AUTHOR_GROUP, 'CODE', 'facetAuthor') : '');


    // 발행자 패싯 세팅
    let hasPublisherGroup = !isEmptyList && (facetList.PUBLISHER_GROUP && 0 < facetList.PUBLISHER_GROUP.length);
    facetHtml = facetHtml.replace('{PUBLISHER_FACET_DATA}', hasPublisherGroup ? createFacetListHtml(facetList.PUBLISHER_GROUP, 'CODE', 'facetPublisher') : '');

    // 발행년 패싯 세팅
    let hasPubYearGroup = !isEmptyList && (facetList.PUB_YEAR_GROUP && 0 < facetList.PUB_YEAR_GROUP.length);
    facetHtml = facetHtml.replace('{PUB_YEAR_FACET_DATA}', hasPubYearGroup ? createFacetListHtml(facetList.PUB_YEAR_GROUP, 'CODE', 'facetPubYear') : '');

    // 주제별 분류 패싯 세팅
    let hasSubjectCode = !isEmptyList && (facetList.SUBJECT_CODE && 0 < facetList.SUBJECT_CODE.length);
    facetHtml = facetHtml.replace('{SUBJECT_FACET_DATA}',  hasSubjectCode ? createFacetListHtml(facetList.SUBJECT_CODE, 'NAME', 'facetSubject') : '');

    // 매체구분 패싯 세팅
    let hasMediaGroup = !isEmptyList && (facetList.MEDIA_GROUP && 0 < facetList.MEDIA_GROUP.length);
    facetHtml = facetHtml.replace('{MEDIA_FACET_DATA}', hasMediaGroup ? createFacetListHtml(facetList.MEDIA_GROUP, 'NAME', 'facetMedia') : '');

    // 초기화
    document.getElementById('facetDiv').innerHTML = '';

    if (searchParams && (searchParams.facetLib || searchParams.facetAuthor || searchParams.facetPubYear ||
        searchParams.facetPublisher || searchParams.facetSubject || searchParams.facetMedia)) {

        let limitsHtml = document.getElementById('template-limits-item').innerHTML;
        limitsHtml = limitsHtml.replace('{LIMIT_CONTENTS}', createFacetLimitHtml(searchParams));
        document.getElementById('facetDiv').innerHTML = limitsHtml;
    }

    // 최종 반영
    document.getElementById('facetDiv').innerHTML += facetHtml;

    // set facet header events
    let dtElements = document.querySelectorAll("#facetDiv dt");
    for (let i = 0 ; i < dtElements.length; i++ ) {

        dtElements[i].removeEventListener('click', showAllFacet);
        if (!isEmptyList) {
            dtElements[i].addEventListener('click', showAllFacet);
        }
    }

    // set facet elements events
    let ddElements = document.querySelectorAll("#facetDiv .searchFacet");
    for (let i = 0 ; i < ddElements.length; i++ ) {
        ddElements[i].removeEventListener('click', searchFacet);
        if(!isEmptyList) {
            ddElements[i].addEventListener('click', searchFacet);
        }
    }
}

function createFacetLimitHtml(searchParams) {

    let limitHtmlArr = [];

    if (searchParams.facetLib) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetLibName));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetLib\');">삭제</a></li>');
    }

    if (searchParams.facetAuthor) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetAuthor));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetAuthor\');">삭제</a></li>');
    }

    if (searchParams.facetPubYear) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetPubYear));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetPubYear\');">삭제</a></li>');
    }

    if (searchParams.facetPublisher) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetPublisher));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetPublisher\');">삭제</a></li>');
    }

    if (searchParams.facetSubject) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetSubjectName));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetSubject\');">삭제</a></li>');
    }

    if (searchParams.facetMedia) {
        limitHtmlArr.push('<li><span>');
        limitHtmlArr.push(decodeURI(searchParams.facetMediaName));
        limitHtmlArr.push('</span><a href="javascript:removeFacetLimitElement(\'facetMedia\');">삭제</a></li>');
    }

    return limitHtmlArr.join('');

}

function removeFacetLimitElement(type) {
    if ('facetLib' === type ) {
        GLOBAL_FACETS.facetLib = '';
        GLOBAL_FACETS.facetLibName = '';
    } else if ('facetAuthor' === type ) {
        GLOBAL_FACETS.facetAuthor = '';
    } else if ('facetPubYear' === type ) {
        GLOBAL_FACETS.facetPubYear = '';
    } else if ('facetPublisher' === type ) {
        GLOBAL_FACETS.facetPublisher = '';
    } else if ('facetSubject' === type ) {
        GLOBAL_FACETS.facetSubject = '';
        GLOBAL_FACETS.facetSubjectName = '';
    } else if ('facetMedia' === type ) {
        GLOBAL_FACETS.facetMedia = '';
        GLOBAL_FACETS.facetMediaName = '';
    }

    search(false, true);
}

/**
 * 기본 5개를 초과하는 패싯 정보를 보여줌
 * @param evt
 */
function showAllFacet(evt) {

    let dt = evt.target.tagName === 'H5' ? evt.target.parentNode : evt.target;
    let isOpen = ($(dt).hasClass("on") == 1);
    if(isOpen)
        $(dt).removeClass('on');
    else
        $(dt).addClass('on');

    let dl = dt.parentNode;
    let dds = dl.querySelectorAll('dd');
    for (let i = 0 ; i< dds.length; i++ ) {
        let dd = dds[i];
        if ( dd.className.indexOf('top') > -1 ) continue;
        $(dd).removeClass('hidden');
        if(isOpen){
            $(dd).addClass('hidden');
        }
    }
}

/**
 * 패싯 안에 더보기 버튼을 통한 더 많은 패싯 정보를 보여줌
 * @param evt
 */
function moreAllFacet(evt) {

    let moreBtnDD = evt.parentNode;
    let isOpen = ($(moreBtnDD).hasClass("on") == 1);
    if(isOpen) {
        $(moreBtnDD).removeClass('on');
        $(evt).prev().removeClass("hidden");
        $(evt).addClass("hidden");
    } else {
        $(moreBtnDD).addClass('on');    	$(evt).next().removeClass("hidden");
        $(evt).addClass("hidden");
    }

    let dl = moreBtnDD.parentNode;
    let dds = dl.querySelectorAll('dd');
    for (let i = 5 ; i< dds.length-1; i++ ) {
        var dd = $(dds[i]);
        dd.removeClass('off');
        dd.removeClass('hidden');
        if(isOpen){
            dd.addClass('off');
        }
    }
}

/***
 * 패싯 검색
 * @param evt
 */
function searchFacet(evt) {

    evt.preventDefault();

    let t = evt.target;
    let group  = t.getAttribute('facet-group');
    let code  = t.getAttribute('facet-code');
    let desc  = t.getAttribute('facet-desc');

    if ('facetLib' === group) {
        GLOBAL_FACETS.facetLib = code;
        GLOBAL_FACETS.facetLibName = desc;
    } else if ('facetAuthor' === group) {
        GLOBAL_FACETS.facetAuthor = code;
    } else if ('facetPubYear' === group) {
        GLOBAL_FACETS.facetPubYear = code;
    } else if ('facetPublisher' === group) {
        GLOBAL_FACETS.facetPublisher = code;
    } else if ('facetSubject' === group) {
        GLOBAL_FACETS.facetSubject = code;
        GLOBAL_FACETS.facetSubjectName = desc;
    } else if ('facetMedia' === group) {
        GLOBAL_FACETS.facetMedia = code;
        GLOBAL_FACETS.facetMediaName = desc;
    }

    search(($("#isInnerChk").val() == "true") ? true : false, true);
}
/**
 * 패싯 검색
 */
function searchFacetPage(evt) {
    search(($("#isInnerChk").val() == "true") ? true : false, false);
}
/**
 * 패싯 컨텐츠 생성
 * @param dataList
 * @param valueKey
 * @param facetGroup
 * @returns {string}
 */
function createFacetListHtml ( dataList, valueKey, facetGroup ) {
    let len = dataList.length;
    let htmlArr = new Array();

    for (let i = 0 ; i < len ; i++  ) {
        let data = dataList[i];
        let cntHtml = document.getElementById('template-facet-count-item').innerHTML;
        htmlArr.push('<dd');
        if (i > 4) {
            htmlArr.push(' class="hidden off">');
        } else {
            htmlArr.push('>');
//        	  htmlArr.push(' class="top">');
        }
        htmlArr.push('<a href="#none" class="searchFacet" ');
        htmlArr.push(' facet-group="');
        htmlArr.push(facetGroup);
        htmlArr.push('" facet-code="');
        htmlArr.push(encodeURI(data['CODE']));
        htmlArr.push('" facet-desc="');
        htmlArr.push(encodeURI(data[valueKey]));
        htmlArr.push('">');
        htmlArr.push(data[valueKey]);
        htmlArr.push(cntHtml.replace("{FACET_COUNT}", data.COUNT));
        htmlArr.push('</a>');
        htmlArr.push('</dd>');
    }
    if(len > 5){
        htmlArr.push('<dd class="facet_more"><button onclick="moreAllFacet(this);">더보기</button>');
        htmlArr.push('<button class="hidden" onclick="moreAllFacet(this);">닫기</button></dd>');
    }
    return htmlArr.join('');
}


/**
 * 검색목록 세팅
 * @param dataList
 */
function createContentElements(dataList, userNo, userClassCode) {

    const kind = getSearchKind();
    let innerArr = new Array();

    if ('book' === kind ) {
        for(let i = 0 ; i < dataList.length ; i++ ) {
            const bookData = dataList[i];
            let html = document.getElementById("template-book-item").innerHTML;
            // html = html.replace("{IMAGE}", bookData.IMAGE);
            html = html.replace("{IMAGE}", "<a href='#' onclick=\"getBookDetail('"+bookData.ISBN+"','"+bookData.BOOK_KEY+"'); return false;\"><img src='"+bookData.IMAGE+"' alt='표지'></a>");
            html = html.replace("{LIB_TYPE_CLASS}", getTagData(bookData.COLOR, 'LIB_TYPE_CLASS'));
            html = html.replace("{LIB_NAME}", getTagData(bookData.LIB_NAME, 'LIB_NAME'));
            // html = html.replace("{TITLE_INFO}", getTagData(bookData.TITLE_INFO, 'TITLE_INFO'));
            html = html.replace("{TITLE_INFO}", "<a href='#' onclick=\"getBookDetail('"+bookData.ISBN+"','"+bookData.BOOK_KEY+"'); return false;\">"+bookData.TITLE_INFO+"</a>");
            html = html.replace("{AUTHOR_INFO}", getTagData(bookData.AUTHOR, 'AUTHOR_INFO'));
            html = html.replace("{PUBLISHER}", getTagData(bookData.PUBLISHER, 'PUBLISHER'));
            html = html.replace("{PUBLISH_YEAR}", getTagData(bookData.PUB_YEAR, 'PUBLISH_YEAR'));
            html = html.replace("{SHELF_LOC_CODE}", getTagData(bookData.SHELF_LOC_GROUP, 'SHELF_LOC_CODE'));
            html = html.replace("{CALL_NO}", getTagData(bookData.CALL_NO, 'CALL_NO'));
            html = html.replace("{REG_NO}", getTagData(bookData.REG_NO, 'REG_NO'));
            html = html.replace("{ISBN}", getTagData(bookData.ISBN, 'ISBN'));
            html = html.replace("{KEYWORD}", getKeywords(bookData));
            html = html.replace("{SERIES_INFO}", getTagData(bookData, 'SERIES_INFO'));
            html = html.replace("{APPENDIX_INFO}", getAppendixInfo(bookData));
            html = html.replace("{BOOK_KEY}", getTagData(bookData.BOOK_KEY, 'BOOK_KEY'));
            html = html.replace("{SPECIES_KEY}", getTagData(bookData.SPECIES_KEY, 'SPECIES_KEY'));

            html = html.replace("{LOAN_STATUS}", getLoanStatus(bookData));
            html = html.replace("{BUTTONS}", setBookButtons(bookData, userNo, userClassCode));
            html = html.replace("{FAVORITE_BUTTON}",setFavoriteButton(bookData, userNo, userClassCode));

            html = html.replaceAll("{LIB_BOOK_KEY}", bookData.BOOK_KEY);
            // html = html.replaceAll("{BOOK_ISBN}", bookData.ISBN);
            innerArr.push(html);
        }

        document.getElementById('bookList').innerHTML = innerArr.join('');

    } else if ('nonbook' === kind ) {
        for(let i = 0 ; i < dataList.length ; i++ ) {
            const data = dataList[i];
            let html = document.getElementById("template-nonbook-item").innerHTML;
            html = html.replace("{IMAGE}", data.IMAGE);
            html = html.replace("{LIB_TYPE_CLASS}", getTagData(data.COLOR, 'LIB_TYPE_CLASS'));
            html = html.replace("{LIB_NAME}", getTagData(data.LIB_NAME, 'LIB_NAME'));
            html = html.replace("{TITLE_INFO}", getTagData(data.TITLE_INFO, 'TITLE_INFO'));
            html = html.replace("{AUTHOR_INFO}", getTagData(data.AUTHOR, 'AUTHOR_INFO'));
            html = html.replace("{PUBLISHER}", getTagData(data.PUBLISHER, 'PUBLISHER'));
            html = html.replace("{PUBLISH_YEAR}", getTagData(data.PUB_YEAR, 'PUBLISH_YEAR'));
            html = html.replace("{SHELF_LOC_CODE}", getTagData(data.SHELF_LOC_GROUP, 'SHELF_LOC_CODE'));
            html = html.replace("{CALL_NO}", getTagData(data.CALL_NO, 'CALL_NO'));
            html = html.replace("{REG_NO}", getTagData(data.REG_NO, 'REG_NO'));
            html = html.replace("{USE_LIMIT_DESC}", getTagData(data.USE_LIMIT_DESC, 'USE_LIMIT_DESC'));
            html = html.replace("{FORM_DESC}", getTagData(data.NONBOOK_FORM, 'FORM_DESC'));
            html = html.replace("{GENRE_DESC}", getTagData(data.NONBOOK_GENRE, 'GENRE_DESC'));
            html = html.replace("{LANGUAGE_SUB}", getTagData(data, 'LANGUAGE_SUB'));
            html = html.replace("{AWARDS}", getTagData(data.NONBOOK_AWARDS, 'AWARDS'));
            html = html.replace("{KEYWORD}", getKeywords(data));


            html = html.replace("{LOAN_STATUS}", getLoanStatus(data));
            html = html.replace("{BUTTONS}", setBookButtons(data, userNo, userClassCode));

            html = html.replace("{ISBN}", getTagData(data.ISBN, 'ISBN'));
            html = html.replace("{APPENDIX_INFO}", getAppendixInfo(data));
            html = html.replaceAll("{LIB_BOOK_KEY}", data.BOOK_KEY);

            innerArr.push(html);
        }

        document.getElementById('nonBookList').innerHTML = innerArr.join('');
    } else if ('ebook' === kind ) {
        for(let i = 0 ; i < dataList.length ; i++ ) {
            const data = dataList[i];
            let html = document.getElementById("template-ebook-item").innerHTML;
            html = html.replace("{IMAGE}", data.IMAGE);
            html = html.replace("{LIB_TYPE_CLASS}", getTagData(data.COLOR, 'LIB_TYPE_CLASS'));
            html = html.replace("{LIB_NAME}", getTagData(data.LIB_NAME, 'LIB_NAME'));
            html = html.replace("{TITLE_INFO}", getTagData(data.TITLE_INFO, 'TITLE_INFO'));
            html = html.replace("{AUTHOR_INFO}", getTagData(data.AUTHOR, 'AUTHOR_INFO'));
            html = html.replace("{PUBLISHER}", getTagData(data.PUBLISHER, 'PUBLISHER'));
            html = html.replace("{PUBLISH_YEAR}", getTagData(data.PUB_YEAR, 'PUBLISH_YEAR'));
            html = html.replace("{KEYWORD}", getKeywords(data));
            if(data.BARCODE) {
                const barcode = String(data.BARCODE).replace(/\\/g, "\\\\").replace(/'/g, "\\'");
                html = html.replace("{BUTTONS}", "<button class=\"ebook_link\"" + "onclick=\"goEBookLink('" + barcode + "')\">전자책바로가기</button>");
            } else {
                html = html.replace("{BUTTONS}", "<button class=\"reserv_impossibl\")>전자책바로가기</button>");
            }
            innerArr.push(html);
        }

        document.getElementById('eBookList').innerHTML = innerArr.join('');
    } else {
        for(let i = 0 ; i < dataList.length ; i++ ) {
            const data = dataList[i];
            let html = document.getElementById("template-serial-item").innerHTML;
            html = html.replace("{IMAGE}", data.IMAGE);
            html = html.replace("{LIB_TYPE_CLASS}", getTagData(data.COLOR, 'LIB_TYPE_CLASS'));
            html = html.replace("{LIB_NAME}", getTagData(data.LIB_NAME, 'LIB_NAME'));
            html = html.replace("{TITLE_INFO}", getTagData(data.TITLE_INFO, 'TITLE_INFO'));
            html = html.replace("{AUTHOR_INFO}", getTagData(data.AUTHOR, 'AUTHOR_INFO'));
            html = html.replace("{PUBLISHER}", getTagData(data.PUBLISHER, 'PUBLISHER'));
            html = html.replace("{PUBLISH_YEAR}", getTagData(data.PUB_YEAR, 'PUBLISH_YEAR'));
            html = html.replace("{VOL_TITLE}", getTagData(data, 'VOL_TITLE'));
            html = html.replace("{SHELF_LOC_CODE}", getTagData(data.SHELF_LOC_NAME, 'SHELF_LOC_CODE'));
            html = html.replace("{ISSN}", getTagData(data.ISSN, 'ISSN'));

            // html = html.replace("{LOAN_STATUS}", getLoanStatus(data));
            html = html.replace("{MORE_SERIES_BTN}", getMoreSeriesBtn(data));

            innerArr.push(html);
        }

        document.getElementById('serialList').innerHTML = innerArr.join('');
    }

}

// HTML 태그 제거 유틸
function stripHtml(html) {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

function setFavoriteButton(bookData, userNo) {

    if(login_memberClass == "2" || isNullCheck(userNo) || isNullChange(userNo) === "없음"){
        return '';
    } else {
        if (isNullCheck(userNo) || isNullChange(userNo) === "없음") {
            return `<div class="favorite_wrap"> 
                    <button class="button"
                            data-params="${encodeURIComponent(JSON.stringify(getFavoriteButtonParams(bookData)))}"
                            onclick="openLoginPop();">
                        <span>찜하기</span>
                    </button>
                </div>`;
        }

        if (!bookData) return '';
        const params = getFavoriteButtonParams(bookData);

        if (bookData.ALREADY_IN_BOOKCASE) {
            return `<div class="favorite_wrap">
                     <button class="button on"
                    data-params="${encodeURIComponent(JSON.stringify(params))}"
                    onclick="favorite(this,'0', function() { popCloseSearch(); })">
                <span>찜하기</span>
            </button>
                </div>`;
        } else {
            return `
            <div class="favorite_wrap">
                <button class="button"
                        data-params="${encodeURIComponent(JSON.stringify(params))}"
                        onclick="favorite(this,'0', function() { popCloseSearch(); })">
                    <span>찜하기</span>
                </button>
            </div>`;
        }
    }
}

// 찜하기 버튼의 파라미터 추출
function getFavoriteButtonParams(bookData) {
    return {
        book_key: bookData.BOOK_KEY,
        species_key: bookData.SPECIES_KEY,
        isbn: bookData.ISBN,
        title: stripHtml(bookData.TITLE_INFO),
        author: stripHtml(bookData.AUTHOR),
        publisher: bookData.PUBLISHER,
        pub_year: bookData.PUB_YEAR,
        pub_form_code: bookData.FORM_CODE,
        contents_type: bookData.FORM_CODE === "MO" ? "단행본" : bookData.FORM_CODE === "SE" ? "연속" : bookData.FORM_CODE === "NB" ? "비도서" : "기타",
        coverUrl: bookData.IMAGE,
        call_no: bookData.CALL_NO,
        lib_name: bookData.LIB_NAME,
        shelf_loc_name: bookData.SHELF_LOC_CODE,
        loan_status: bookData.LOAN_STATUS,
        manage_code: bookData.MANAGE_CODE,
        reserve_code: bookData.RESERVE_CODE
    };
}
/* on 클래스 추가 시 하트 색깔 빨간색으로 변경 */

function setBookButtons(bookData, userNo, userClassCode) {

    if (!bookData) return '';

    const loanCode = bookData.LOAN_CODE;
    let buttonArr = [];

    // 로그인 한 사용자
    if (userNo && login_memberClass != "2" && bookData.MANAGE_CODE !== "141674" && bookData.MANAGE_CODE !== "150018" && bookData.MANAGE_CODE !== "144011" && bookData.MANAGE_CODE !== "311867") {
        if("Y" === bookData.KBILL_YN && "Y" === bookData.KBILL_REQUEST_USE_YN && !isNullCheck(login_user_no) &&"OK" == loanCode && bookData.MANAGE_CODE != "141108"){ // 141108 : 화홍어린이도서관
            //buttonArr.push("<button onclick=\"openLillPop('"+bookData.MANAGE_CODE+"',"+bookData.BOOK_KEY+",function() { popCloseSearch();})\">"+getLillServiceName()+"신청</button>");
            buttonArr.push(
                "<button onclick=\"openLillPop('"
                + bookData.MANAGE_CODE + "', "
                + bookData.BOOK_KEY
                + ", function() { popCloseSearch(); });\">"
                + getLillServiceName() + "신청</button>"
            );
        } else {
            buttonArr.push("<button class=\"reserv_impossibl\">"+getLillServiceName()+"신청</button>");
        }

        if ("Y" === bookData.RESERVATION_YN && getReservationStatus(bookData) && !isNullCheck(login_user_no) && reserveManageCodeCheck(bookData) === "Y") {
            buttonArr.push('<button onclick="openReservePop('+bookData.BOOK_KEY+',function() { popCloseSearch();})">예약하기</button>');
        }
        else {
            let resCnt = bookData.RESERVATION_CNT;
            let resNum = bookData.RESERVATION_NUMBER;
            if(!isNullCheck(resCnt) && !isNullCheck(resNum) && resNum > 0 && resCnt == resNum){
                buttonArr.push("<button class=\"reserv_impossibl\" onclick=\"alert('허용 가능한 예약 인원이 초과 하였습니다. ("+resCnt+"/"+resNum+")');\">예약하기</button>");
            } else {
                buttonArr.push("<button class=\"reserv_impossibl\">예약하기</button>");
            }
        }

        // if(bookData.RESERVE_CODE == 'NOT_ALLOWED_NORMAL') {
        //     buttonArr.push("<button  onclick=\"alert('예약 불가한 자료입니다..');\">예약하기</button>");
        // }

        if ("Y" === bookData.UNMANNED_RESERVATION_YN && unmannedReserveManageCodeCheck(bookData) === 'Y' && !isNullCheck(login_user_no)) {
            if (getUnmannedReservetionStatus(bookData) && bookData.LOAN_CODE == "OK" && bookData.FORM_CODE == "BK") {
                buttonArr.push(
                    "<button onclick=\"openUnmannedReservePop("
                    + bookData.BOOK_KEY + ", '"
                    + bookData.MANAGE_CODE + "', '"
                    + bookData.IMAGE + "', '"
                    + bookData.LIB_NAME
                    + "', function() { popCloseSearch(); });"
                    + "\">책나루(무인)예약</button>"
                );
            } else {
                buttonArr.push('<button class="reserv_impossibl">책나루(무인)예약</button>');
            }
        } else {
            buttonArr.push('<button class="reserv_impossibl">책나루(무인)예약</button>');
        }
    }

    if (bookData.ISBN) {
        buttonArr.push('<button class="addInfo" onclick="getLibBookInfo(\''+bookData.BOOK_KEY+'\',\''+bookData.ISBN+'\',\''+bookData.FORM_CODE+'\')" id="libBookBtn_'+bookData.BOOK_KEY+'">소장정보</button>');
    }


    return buttonArr.join('');
}

function reserveNoAlert(){
    alert("예약가능한 자료가 아닙니다.");
}

function getLibBookInfo(book_key,isbn,form_code) {
    let functionName="소장정보";
    if($("#libBookBtn_" + book_key).hasClass("on")){
        $("#bookHaveList_" + book_key).hide();
        $("#libBookBtn_" + book_key).removeClass("on");
        return;
    }
    let bookListHtml = "";
    let libListHtml = "";

    $.ajax({
        type : 'post',
        url  : getContextPath()+'/search/get/lib/bookinfo',
        data : {"book_isbn":isbn, "book_form_code" : form_code},
        success : function(data){
            insertFunctionLog(functionName);
            let libListCnt = data.libList.length;
            libListHtml = "<div class=\"check all hidden\"><input type=\"checkbox\" name=\"library_" + book_key + "\" value=\"\" id=\"checkAll_" + book_key + "\" checked><label for=\"checkAll_" + book_key + "\">전체선택</label></div>";
            for(let i = 0; i < libListCnt; i++){
                if(i > 6){
                    libListHtml += "<div class=\"check more hidden\"><input type=\"checkbox\" name=\"library_" + book_key + "\" value=\"" + book_key + "_" + data.libList[i].MANAGE_CODE + "\" id=\"chk_" + book_key + i + "\" checked><label for=\"chk_" + book_key + i + "\">" + data.libList[i].NICKNAME + "(" + data.libList[i].BOOK_COUNT + ")</label></div>";
                } else {
                    libListHtml += "<div class=\"check hidden\"><input type=\"checkbox\" name=\"library_" + book_key + "\" value=\"" + book_key + "_" + data.libList[i].MANAGE_CODE + "\" id=\"chk_" + book_key + i + "\" checked><label for=\"chk_" + book_key + i + "\">" + data.libList[i].NICKNAME + "(" + data.libList[i].BOOK_COUNT + ")</label></div>";
                }

            }
            if(libListCnt > 6) {
                libListHtml += "<div class=\"addlist\"><button type=\"button\" id=\"libOpenBtn_" + book_key + "\" onclick='clickLibMore(\""+book_key+"\")'><span>+ 더보기</span></div>";
            }
            let bookListCnt = data.bookList.length;
            for(let i = 0; i < bookListCnt; i++){
                bookListHtml +="<div class=\"libInfoBox\" name='libInfoBox_"+book_key+"_"+data.bookList[i].MANAGE_CODE+"'><div class=\"textInfo\">"+getLibLoanStatus(data.bookList[i]);
                bookListHtml +="<p class=\"libTitle lib_type" + data.bookList[i].LIB_TYPE_COLOR + "\">"+data.bookList[i].LIB_NAME+"</p>";
                bookListHtml +="<p>"+data.bookList[i].SHELF_LOC_GROUP+"</p>";
                bookListHtml +="<p>"+data.bookList[i].CALL_NO+"</p></div>";

                bookListHtml += "<div class=\"buttonArea\">";

                if(login_memberClass == "2" || data.bookList[i].MANAGE_CODE == "141674" || data.bookList[i].MANAGE_CODE == "150018" || data.bookList[i].MANAGE_CODE == "144011" || data.bookList[i].MANAGE_CODE == "311867") {
                    bookListHtml += "<button type=\"button\" onclick=\"reserveNoAlert()\" style=\"opacity:0.5; pointer-events:none;\">예약하기</button>";
                    bookListHtml += "<button type=\"button\" style=\"opacity:0.5; pointer-events:none;\">상호대차신청</button>";
                    bookListHtml += "<button type=\"button\" onclick=\"reserveNoAlert()\" style=\"opacity:0.5; pointer-events:none;\">책나루(무인)예약</button>";
                } else {

                    if ("Y" === data.bookList[i].RESERVATION_YN && getReservationStatus(data.bookList[i]) && !isNullCheck(login_user_no) && reserveManageCodeCheck(data.bookList[i]) === "Y") {
                        bookListHtml += "<button type=\"button\" onclick=\"openReservePop(" + data.bookList[i].BOOK_KEY + ",function() { popCloseSearch();})\">예약하기</button>";
                    } else {
                        let resCnt = data.bookList[i].RESERVATION_CNT;
                        let resNum = data.bookList[i].RESERVATION_NUMBER;

                        if (!isNullCheck(resCnt) && !isNullCheck(resNum) && resNum > 0 && resCnt == resNum) {
                            bookListHtml += "<button type=\"button\" onclick=\"alert('허용 가능한 예약 인원이 초과 하였습니다. (" + resCnt + "/" + resNum + ")');\" style=\"opacity:0.5;\">예약하기</button>";
                        } else {
                            bookListHtml += "<button type=\"button\" onclick=\"reserveNoAlert()\" style=\"opacity:0.5; pointer-events:none;\">예약하기</button>";
                        }


                    }
                    if ("Y" === data.bookList[i].KBILL_YN && "Y" === data.bookList[i].KBILL_REQUEST_USE_YN && !isNullCheck(login_user_no) && "OK" == data.bookList[i].LOAN_CODE && data.bookList[i].MANAGE_CODE != "141108") {
                        //bookListHtml += "<button type=\"button\" onclick=\"openLillPop('" + data.bookList[i].MANAGE_CODE + "'," + data.bookList[i].BOOK_KEY + ",function() { popCloseSearch();})\">" + getLillServiceName() + "<br>신청</button>";
                        bookListHtml +=
                            "<button type=\"button\" onclick=\" openLillPop('"
                            + data.bookList[i].MANAGE_CODE + "',"
                            + data.bookList[i].BOOK_KEY
                            + ", function() { popCloseSearch(); });\">"
                            + getLillServiceName() + "<br>신청</button>";
                    } else {
                        bookListHtml += "<button type=\"button\" style=\"opacity:0.5; pointer-events:none;\">상호대차신청</button>";
                    }


                    if ("Y" === data.bookList[i].UNMANNED_RESERVATION_YN && unmannedReserveManageCodeCheck(data.bookList[i]) === 'Y' && !isNullCheck(login_user_no)) {
                        if (getUnmannedReservetionStatus(data.bookList[i]) && data.bookList[i].LOAN_CODE == "OK" && data.bookList[i].FORM_CODE == "BK") {
                            bookListHtml +=
                                "<button type=\"button\" onclick=\"openUnmannedReservePop("
                                + data.bookList[i].BOOK_KEY + ", '"
                                + data.bookList[i].MANAGE_CODE + "', '"
                                + data.bookList[i].IMAGE + "', '"
                                + data.bookList[i].LIB_NAME + "', function() { popCloseSearch(); });"
                                + "\">책나루<br>(무인)예약</button>";
                        } else {
                            bookListHtml += "<button type=\"button\" onclick=\"reserveNoAlert()\" style=\"opacity:0.5; pointer-events:none;\">책나루(무인)예약</button>";
                        }
                    } else {
                        bookListHtml += "<button type=\"button\" onclick=\"reserveNoAlert()\" style=\"opacity:0.5; pointer-events:none;\">책나루(무인)예약</button>";
                    }
                }
                bookListHtml += "</div>";
                bookListHtml += "</div>";
            }

            $("#chkLibListCount_"+book_key).html(libListCnt);
            $("#chkLibList_" + book_key).html(libListHtml);
            $("#chkLibBookList_" + book_key).html(bookListHtml);
            $("#bookHaveList_" + book_key).show();
            $("#libBookBtn_" + book_key).addClass("on");

            $("#chkLibList_" + book_key).on('change', "#checkAll_" + book_key, function() {
                let checked = $(this).is(":checked");
                // 같은 이름 체크박스 모두 체크/해제 (전체선택 제외 자기 자신은 제외)
                $("#chkLibList_" + book_key + " input[type='checkbox'][name='library_" + book_key + "']").not(this).prop("checked", checked).trigger('change');
            });
            // 개별 체크박스 change 이벤트
            $("#chkLibList_" + book_key).find("input[type='checkbox'][name='library_" + book_key + "']").not("#checkAll_" + book_key).on('change', function() {
                let selectedValues = [];

                // 선택된 체크박스 value 수집
                $("#chkLibList_" + book_key + " input[type='checkbox'][name='library_" + book_key + "']:checked").not("#checkAll_" + book_key).each(function() {
                    selectedValues.push($(this).val());
                });

                // 모두 체크됐으면 전체선택 체크표시, 아니면 해제
                let allChecked = $("#chkLibList_" + book_key + " input[type='checkbox'][name='library_" + book_key + "']").not("#checkAll_" + book_key).length === selectedValues.length;
                $("#checkAll_" + book_key).prop("checked", allChecked);

                // 모든 libInfoBox 숨기기
                $("div[name^='libInfoBox_" + book_key + "_']").hide();

                // 선택된 체크박스 값에 해당하는 libInfoBox 보이기
                selectedValues.forEach(function(value) {
                    $("div[name='libInfoBox_" + value + "']").show();
                });
            });
        },
        error : function(response){
            ajaxErrorMsg(response, false);
        }
    });
}
function clickLibMore(book_key) {
    $("#chkLibList_" + book_key).find(".more").removeClass("hidden");
    $("#libOpenBtn_" + book_key).parent().hide();
}

function getLibLoanStatus(data) {

    const loanCode = data.LOAN_CODE;
    const returnPlanDate = data.RETURN_PLAN_DATE;
    let htmlArr = ['<p '];

    let useLimitCode = data.USE_LIMIT_CODE;
    let LIB_RESERVATION_YN = data.LIB_RESERVATION_YN; // 예약 가능 여부

    //BOOK_RETURN_PLAN_DATE
    if('OK' === loanCode){
        htmlArr.push('class="state on"><span>대출가능(비치중)</span>');
    }else if('BROKEN' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(파손자료)</span>');
    }else if('OTHER_LOAN' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(타관대출중)</span>');
    }else if('OTHER_LOAN_READY' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(타관대출 대기중)</span>');
    }else if('OTHER_RETURN' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(타관반납중)</span>');
    }else if('RESERVE_LOAN_READY' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(예약대출 대기중)</span>');
    }else if('NOT_ALLOWED' === loanCode){
        if ('CD' === useLimitCode) {
            htmlArr.push('class="state off"><span>대출불가(관내열람)</span>');
        } else {
            htmlArr.push('class="state off"><span>대출불가</span>');
        }
    }else if('OUT_ON_LOAN' === loanCode){
        htmlArr.push('class="state off"><span>대출불가(대출중)</span>');
    } else {
        htmlArr.push('>');
    }

    if ('OK' !== loanCode && returnPlanDate) {
        htmlArr.push('<span class="date">반납예정</span>');
        htmlArr.push('<strong>' + returnPlanDate + '</strong>');
    }

    htmlArr.push('</p>');
    return htmlArr.join('');
}



/**
 * 다른권호 더보기 버튼 세팅
 * @param data
 */
function getMoreSeriesBtn(data) {
    return '<button onclick="getMoreSeriesPopup('+data.SPECIES_KEY+'); ">다른권호더보기</button>';
}

/**
 * 도서관 목록 펼치기 이벤트
 */
function openLibList(type) {
    if(type === "detail"){
        $("#detailLibraries").removeClass("close")
        $("#detailLibraries").addClass("open");
        $("#openDetailLibList").addClass("hidden");
        $("#closeDetailLibList").removeClass("hidden");
    } else {
        $("#normalLibraries").removeClass("close")
        $("#normalLibraries").addClass("open");
        $("#openLibList").addClass("hidden");
        $("#closeLibList").removeClass("hidden");
    }

}

/**
 * 도서관 목록 닫기 이벤트
 */
function closeLibList(type) {
    if(type === "detail"){
        $("#detailLibraries").removeClass("open")
        $("#detailLibraries").addClass("close");
        $("#closeDetailLibList").addClass("hidden");
        $("#openDetailLibList").removeClass("hidden");
    } else {
        $("#normalLibraries").removeClass("open")
        $("#normalLibraries").addClass("close");
        $("#closeLibList").addClass("hidden");
        $("#openLibList").removeClass("hidden");
    }
}

/**
 * 데이터에 대한 태그 세팅 조회
 * @param data
 * @param type
 * @returns {string}
 */
function getTagData(data, type) {

    let htmlArr = [];
    if ( 'LIB_NAME' === type || 'TITLE_INFO' === type ) {
        htmlArr.push(data);
    }
    if ( 'LIB_TYPE_CLASS' === type && data) {
        htmlArr.push('lib_type' + data);
    } else if ( 'AUTHOR_INFO' === type && data) {
        htmlArr.push('<dl class="author"><dt>저자</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'PUBLISHER' === type && data) {
        htmlArr.push('<dl class="publisher"><dt>발행처</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'PUBLISH_YEAR' === type && data) {
        htmlArr.push('<dl class="publishYear"><dt>발행년</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'SHELF_LOC_CODE' === type  && data ) {
        htmlArr.push('<dl class="shelfLoc"><dt>자료위치</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'CALL_NO' === type  && data) {
        htmlArr.push('<dl class="callNo"><dt>청구기호</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'REG_NO' === type  && data) {
        htmlArr.push('<dl class="regNo"><dt>등록번호</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'ISBN' === type  && data ) {
        htmlArr.push('<dl class="isbn"><dt>ISBN</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'SERIES_INFO' === type  && !(isNullCheck(data.SERIES_TITLE) && isNullCheck(data.SERIES_TITLE_NO)) ) {
        htmlArr.push('<dl class="series"><dt>총서명/총서번호</dt><dd>');
        htmlArr.push(data.SERIES_TITLE ? data.SERIES_TITLE : '-');
        htmlArr.push('/');
        htmlArr.push(data.SERIES_TITLE_NO ? data.SERIES_TITLE_NO : '-');
        htmlArr.push('</dd></dl>');
    } else if ( 'USE_LIMIT_DESC' === type  && data ) {
        htmlArr.push('<dl class="useLimit"><dt>이용구분</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'FORM_DESC' === type  && data ) {
        htmlArr.push('<dl class="media"><dt>형태사항</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'GENRE_DESC' === type  && data) {
        htmlArr.push('<dl class="genre"><dt>장르</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'LANGUAGE_SUB' === type  && (data.LANGUAGE || data.SUB_TITLE)) {
        htmlArr.push('<dl class="language"><dt>언어/자막</dt><dd>');
        htmlArr.push(data.LANGUAGE ? data.LANGUAGE : '-');
        htmlArr.push('/');
        htmlArr.push(data.SUB_TITLE ? data.SUB_TITLE : '-');
        htmlArr.push('</dd></dl>');
    } else if ( 'AWARDS' === type  && data ) {
        htmlArr.push('<dl class="awards"><dt>수상내역</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'ISSN' === type  && data) {
        htmlArr.push('<dl class="issn"><dt>ISSN</dt><dd>');
        htmlArr.push(data);
        htmlArr.push('</dd></dl>');
    } else if ( 'VOL_TITLE' === type  && (data.PUBLISH_YEAR && data.VOL_TITLE) ) {
        htmlArr.push('<dl class="volTitle"><dt>최신권호</dt><dd>');
        htmlArr.push(data.PUBLISH_YEAR + '-' + data.VOL_TITLE);
        htmlArr.push('</dd></dl>');
    }

    return htmlArr.join('');
}

function handleTooltipClose(btn) {
    $(btn).closest(".tooltip").removeClass("is-open");
}

$(document).on("mouseenter focus", ".waiting p", function () {
    $(this).next(".tooltip").addClass("is-open");
});

$(document).on("mouseleave", ".waiting", function () {
    $(this).find(".tooltip").removeClass("is-open");
});

// $(document).on("click", ".tooltip button", function () {
//     $(this).closest(".tooltip").removeClass("is-open");
// });
/**
 * 대출상태 세팅
 * @param data
 */
function getLoanStatus(data) {

    const loanCode = data.LOAN_CODE;
    const returnPlanDate = data.RETURN_PLAN_DATE;
    let htmlArr = [];

    let resCnt = data.RESERVATION_CNT;
    let resNum = data.RESERVATION_NUMBER;

    let useLimitCode = data.USE_LIMIT_CODE;
    let LIB_RESERVATION_YN = data.LIB_RESERVATION_YN;

    htmlArr.push('<p ');
    //BOOK_RETURN_PLAN_DATE
    if('OK' === loanCode){
        htmlArr.push('class="borrow_possibl">대출가능<span>(비치중)</span>');
    }else if('BROKEN' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(파손자료)</span>');
    }else if('OTHER_LOAN' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(타관대출중)</span>');
    }else if('OTHER_LOAN_READY' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(타관대출 대기중)</span>');
    }else if('OTHER_RETURN' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(타관반납중)</span>');
    }else if('RESERVE_LOAN_READY' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(예약대출 대기중)</span>');
    }else if('NOT_ALLOWED' === loanCode){
        if ('CD' === useLimitCode) {
            htmlArr.push('class="borrow_impossibl">대출불가<span>(관내열람)</span>');
        } else {
            htmlArr.push('class="borrow_impossibl">대출불가');
        }
    }else if('OUT_ON_LOAN' === loanCode){
        htmlArr.push('class="borrow_impossibl">대출불가<span>(대출중)</span>');
    } else {
        htmlArr.push('>');
    }

    if ('OK' !== loanCode && returnPlanDate) {
        htmlArr.push('<span class="date_title">반납예정 : ');
        htmlArr.push('<strong>' + returnPlanDate + '</strong>');
        htmlArr.push('</span>');
    }

    if(!isNullCheck(resCnt) && !isNullCheck(resNum)){
        htmlArr.push('<div class="waiting">');
        htmlArr.push('<p>예약자수 : ');
        htmlArr.push('<strong>'+resCnt+'</strong>/'+resNum+ '');
        htmlArr.push('</p>');
        htmlArr.push('<div class="tooltip">');
        htmlArr.push('<span>대출중인 자료만 예약가능</span>');
        // htmlArr.push([
        //     '<button type="button" onclick="',
        //     '$(this).closest(\'.tooltip\').removeClass(\'is-open\');',
        //     '"><span>닫기</span></button>'
        // ].join(''));
        htmlArr.push([
            '<button type="button" onclick="handleTooltipClose(this);">',
            '<span>닫기</span>',
            '</button>'
        ].join(''));
        htmlArr.push('</div>');
    }
    htmlArr.push('</p>');

    return htmlArr.join('');
}

/**
 * 예약 가능 상태 세팅
 * @param data
 */
function getReservationStatus(data) {
    const reserveCode = data.RESERVE_CODE;

    if('OK' === reserveCode){
        return true;
    } else if('RESERVE_FULL' === reserveCode){
        return false;
    } else if('RESERVE_REG' === reserveCode){
        return false;
    } else if('RESERVE_SEP_SHELF' === reserveCode){
        return false;
    } else if('RESERVE_LOC' === reserveCode){
        return false;
    } else if('NOT_ALLOWED' === reserveCode){
        return false;
    } else if("NOT_ALLOWED_NORMAL" === reserveCode){
        return false;
    } else if("NOT_LILL_RESERVE" === reserveCode){
        return false;
    } else if("ALREADY_RESERVED" === reserveCode) {
        return false;
    }

    $(".tooltip button").click(function (){
        $(this).parent('.tooltip').hide();
    });

    return false;
}

/**
 * 예약 가능 상태 세팅
 * @param data
 */
function getUnmannedReservetionStatus(data) {
    const reserveCode = data.RESERVE_CODE;

    if (data.UNMANNED_RESERVATION_YN === 'Y' && reserveCode === 'NOT_ALLOWED' && data.LIB_RESERVATION_YN === 'N' && data.LIB_RESERVATION_YN2 === '0') {
        return true;
    }

    if('OK' === reserveCode){
        return true;
    } else if('RESERVE_FULL' === reserveCode){
        return false;
    } else if('RESERVE_REG' === reserveCode){
        return false;
    } else if('RESERVE_SEP_SHELF' === reserveCode){
        return false;
    } else if('RESERVE_LOC' === reserveCode){
        return false;
    } else if('NOT_ALLOWED' === reserveCode){
        return false;
    } else if("NOT_ALLOWED_NORMAL" == reserveCode){
        return true;
    } else if("NOT_LILL_RESERVE" === reserveCode){
        return false;
    }

    return false;
}
/**
 * 일반 예약 사용안하는 도서관 상태 세팅
 * @param data
 */
function reserveManageCodeCheck(data) {
    // 바른샘:141087 슬기샘:141085
    let manageCodeList = [
        "141061",
        "141085",
        "141087",
        "141086",
        "141108"
    ];

    if (manageCodeList.includes(data.MANAGE_CODE)) {
        return 'N';
    } else {
        return 'Y';
    }
}


/**
 * 무인 예약 가능 도서관 상태 세팅
 * @param data
 */
function unmannedReserveManageCodeCheck(data) {
    let manageCodeList = [
        "141061",
        "141064",
        "141138",
        "341147",
        "141107",
        "141108"
    ];

    if (manageCodeList.includes(data.MANAGE_CODE)) {
        return 'N';
    } else {
        return 'Y';
    }
}

/**
 * 부록 정보 세팅
 * @param data
 */
function getAppendixInfo(data) {
    if (data.APPENDIX_TOTAL_CNT && 0 < Number(data.APPENDIX_TOTAL_CNT )) {
        let appendixArr = ['<dl class="appendix"><dt>부록정보</dt><dd>'];
        const appendixInfo = data.APPENDIX_INFO;
        for (let i = 0 ; i < appendixInfo.length ; i++ ) {
            appendixArr.push(appendixInfo[i].DESCRIPTION + '( 수량: ' + appendixInfo[i].APPENDIX_CNT + ' )');
        }
        appendixArr.push('</dd></dl>');
        return appendixArr.join('');
    }

    return '';

}

/**
 * 키워드 세팅
 * @param data
 */
// function looksBroken(s) {
//     return /�/.test(s) || /[?]{3,}/.test(s); // 임시 방편으로 화면에서만 막음
// }
// function getKeywords(data) {
//     const keywords = data.KEYWORD;
//     if (!keywords) return '';
//
//     if (looksBroken(keywords)) {
//         return '';
//     }
//
//     const keywordArr = keywords
//         .split(/\s+/)
//         .filter(Boolean)
//         .map(k => `<a href="javascript:searchKeyword('${escapeJs(k)}');">#${escapeHtml(k)}</a>`)
//         .join('');
//
//     return `<div class="keyword clfix">${keywordArr}</div>`;
// }
//
// function escapeHtml(str) {
//     return str.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
// }
// function escapeJs(str) {
//     return str.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
// }
function getKeywords(data) {
    const keywords = data.KEYWORD;
    if (!keywords) return '';
    const keywordArr = keywords.split(' ').map(keyword => keyword ? '<a href="javascript:searchKeyword(\''+keyword+'\');">#' + keyword + '</a>' : '').join('');
    return ['<div class="keyword clfix">'].concat(keywordArr, ['</div>']).join('');
}

function getKDCSelectInfo(kdc){
    commonAjaxRequest({
        method : 'get',
        url  : getContextPath()+'/popular/get/bestword',
        params : { "manage_code" : globalManageCode , "rank_count" : 10},
        success : function(data){

            let popularEl = document.getElementById('searchPopular');
            popularEl.innerHTML = '';
            let htmlArr = [];

            if(data && data.RESULT_INFO === "SUCCESS" && data.LIST_DATA && 0 < data.LIST_DATA.length){

                popularEl.innerHTML = '<dt>인기검색어</dt>';
                popularEl.style.display = '';
                const rowCnt = data.LIST_DATA.length;

                for( let i = 0; i < rowCnt; i++){
                    const popData = data.LIST_DATA[i];
                    htmlArr.push('<dd><a href="javascript:searchKeyword(\''+popData.SEARCH_WORD+'\')">');
                    htmlArr.push('#'+popData.SEARCH_WORD);
                    htmlArr.push('</a></dd>');
                }

                popularEl.innerHTML += htmlArr.join('');
            }
        }
    });
}
