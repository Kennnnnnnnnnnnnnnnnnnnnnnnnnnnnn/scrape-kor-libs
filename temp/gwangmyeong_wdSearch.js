function wjSearchCheck(f){
	var word = $('#searchWord').val();
	if(word){
		var reg = /[^0-9a-zA-Z_가-힣-\/\:\.\@\!\(\), ]/g;
		word = word.replace(reg,'');
	}
	if(!word){
		alert('검색어를 적어주세요.');
		return false;
	}
	if(word.length == 1){
		//alert('1자이상을 적어주세요.');
		//return false;
	}
	$('#searchWord').attr('value',word);
	if($("#reSearch").is(":checked")){
		$("#reWord").val(word);
		$("#searchWord").attr("disabled","disabled");
		$("#item").attr("disabled","disabled");
	}
	return true;
}
function wjAllChecked(n)
{
	if(n==1) $(".listCheck").attr("checked",true);
	else $(".listCheck").attr("checked",false);
	return false;
}
function wjAllCheckboxNull()
{
	$('input:checkbox:not(checked)').attr("checked", false); 
	$('#searchWord').attr("value","");
}

$(function() {
  $( "#dateS, #dateE " ).datepicker({
  prevText: '이전 달',
  nextText: '다음 달',
  monthNames: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
  monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
  dayNames: ['일','월','화','수','목','금','토'],
  dayNamesShort: ['일','월','화','수','목','금','토'],
  dayNamesMin: ['일','월','화','수','목','금','토'],
  dateFormat: 'yy-mm-dd',
  showMonthAfterYear: true,
  yearSuffix: '년',
  onClose: function( selectedDate ) {
    var option = this.id == "dateS" ? "minDate" : "maxDate";
    var instance = $( this ).data( "datepicker" );
    var date = $.datepicker.parseDate(
        instance.settings.dateFormat ||
        $.datepicker._defaults.dateFormat,
        selectedDate, instance.settings );
	/*
	if($("#"+option)){
	    dates.not( this ).datepicker( "option", option, selectedDate );
	}*/
  }
  });
});



/* 슬라이드(이벤트) */ 
jQuery(function() {
	jQuery("#rolling").jCarouselLite({ //움직여야할 컨텐츠가 있는 부분의 id, class 명을 넣어줌
		btnNext: "#next_button", //다음 버튼 이벤트
		btnPrev: "#prev_button", //이전 버튼 이벤트
		visible: 5, //화면에 보여줄 겟수
		speed: 200, // 슬라이드 동작 속도로 수치가 적을 수록빠름
		circular: false //컨텐츠를 rotation 할건지 결정 하지 않을 경우 false로 교체
	});
});

//검색결과페이지 카테고리 검색 텝
$(document).ready(function(){
	var tab = $(".cate_top li");
	var btn = $(".cate_top li a");
	var list = $(".cate_search01 > ul");
	list,btn.each(function(i)
	{
		var idx = i-1;
		$(this).click(function()
		{
			list.hide().eq(idx).show();
			tab.removeClass("on").addClass("off").eq(idx).removeClass("off").addClass("on");
		});
		idx++;
	});
});


function wdChkLen() {
	var msgtext, msglen;
	var f = document.reviewForm;
	msgtext = f.book_review.value;
	msglen  = f.book_review_len.value;
	var i=0,l=0;
	var temp,lastl;
	//길이를 구한다.
	while(i < msgtext.length){
		temp = msgtext.charAt(i);
		if (escape(temp).length > 4) l+=2;
		else if (temp!='\r') l++;
		// OverFlow
		if(l>200){
			//alert(l);
			alert("소개글 허용 길이 이상의 글을 쓰셨습니다.\n메시지란에는 한글 100자, 영문200자까지만 쓰실 수 있습니다.");
			temp = f.dr_content.value.substr(0,i);
			f.dr_content.value = temp;
			l = lastl;
			break;
		}
		lastl = l;
		i++;
	}
	review_form.book_review_len.value=l;
}

//자료선택
function wjDataChecked(){
	var isCheck = false;
	if(!$('input[name="bookKey[]"]:checked').length){
		alert('하나이상 자료를 선택해 주세요.');
		return false;
	}
	return true;
}

//엑셀 다운로드
function wjXlsCheck(n)
{
	if(wjDataChecked()){
		$('input[name="act"]').val('searchDataXls');
		document.dataRegistForm.submit();
	}
}

