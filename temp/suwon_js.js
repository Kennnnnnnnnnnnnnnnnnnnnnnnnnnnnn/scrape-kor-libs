/**
 * 모바일버전 버튼 슬라이드
 * @param wrapClass 보이거나 가려질 버튼 영역의 지정된 클래스명
 * @param el 클릭한 이벤트 객체
 */
function slideBtn(wrapClass, el){

    if (!wrapClass) return;
    

    const closestWrapperClass = el.parentNode.parentNode.querySelector('.' + wrapClass);
    
    // add on class
    if (el.classList.contains('on')) {
        el.classList.remove('on');
        closestWrapperClass.style.display = 'none';
    } else {
        el.classList.add('on');
        closestWrapperClass.style.display = 'block';
    }

    //const displayEl = closestWrapperClass.style.display;
    
    //closestWrapperClass.style.display = (displayEl ==='block') ? 'none' : 'block';

    const slideTargetBtns = closestWrapperClass.querySelectorAll('button');
    const slideTargetBtnCnt= slideTargetBtns.length;
    if (slideTargetBtnCnt < 2) {
        slideTargetBtns[0].classList.remove('double');
        slideTargetBtns[0].classList.add('single');
    } else {
        for (let i = 0 ; i < slideTargetBtnCnt; i++ ) {
            slideTargetBtns[i].classList.remove('single');
            slideTargetBtns[i].classList.add('double');

        }
    }
}

$(window).resize(function(){
	// 모바일 버튼 영역  화면 커지면 스타일 제거
	if($("body").width() > 1025){
		$(".btn_sR_wrap").removeAttr("style");
		$(".btn_cR_wrap").removeAttr("style");
		$(".btn_arrow_slide.on").removeClass('on');
	}
});