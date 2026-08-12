
//청구기호출력팝업
function fnCallNoPrintPop(bookKey, pubFormCode){
	var url = "/alpasq/popup/callNoPrintPop.do?pubFormCode="+pubFormCode+"&bookKey="+bookKey;
	var objwin = window.open(url, "callNoPrintPop", "resizable=no,status=no,scrollbars=no,toolbar=no,menubar=no,width=360,height=350,left=0,top=0");
	objwin.focus();
}
