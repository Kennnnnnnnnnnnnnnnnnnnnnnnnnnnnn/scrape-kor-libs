from .lib_abs import *
from .util_soup import *
from .util_requests import *

dict_libs = {
'정보과학도서관': {'subdm':'MA'},
'문원도서관': {'subdm':'MW'},
}

class libGwacheon(libAbs):
	area_name = '과천'

	@staticmethod
	def create(_list, val, flag):
		obj = None
		try:
			if dict_libs[val]:
				pass
		except KeyError:
			print("%s doesn't exist" % val)
		else:
			subdm = dict_libs[val]['subdm']
			url_base = "https://www.gclib.go.kr/lib/menu/10008/program/30001/searchResultList.do?viewType=LIST&searchPubFormCode=MO&searchArticle=SCORE&searchOrder=ASC&searchManageCodeArr=%s&" % subdm
			obj = libGwacheon(val, url_base, url_base, flag)
			_list.append(obj)
		return obj

	def __init__(self, name, url_base, url_base_adv, flag):
		numPerPage = 20
		self.url_fmt_num = "&searchDisplay=%d" % numPerPage
		self.url_fmt_type = "&searchType=SIMPLE"
		self.url_fmt_type_a = "&searchType=ADVANCED"
		self.url_fmt_page = "&currentPageNo=%d"
		self.url_fmt_title = "&searchKeyword=%s"
		self.url_fmt_title_a = "&searchAdvTitle=%s"
		self.url_fmt_author = "&searchAdvAuthor=%s"

		#self.path_num = "#searchForm > div > div:nth-of-type(3) > div > div > strong:nth-of-type(2)"
		self.path_num = "#totalCnt"

		# <div id="bookList">
		self.path_root = "#searchForm > div > div:nth-of-type(3) > div:nth-of-type(2) > ul > li"

		# self.path_title = path_aux + " > div:nth-of-type(1) > a > b"
		self.path_title = "div.bookArea > div > div.book_dataInner > a > span.kor.on"
		self.path_author = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info01 > div.kor.on > p:nth-child(1)"
		self.path_publisher = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info01 > div.kor.on > p:nth-child(2)"
		self.path_dec = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info02 > div > p:nth-child(2)"
		self.path_loc = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info03 > div > p"
		self.path_existence = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info04"
		self.path_return = "div.bookArea > div > div.book_dataInner > div.book_info.barList.info04 > div > p:nth-child(2)"

		self.soup_books = None

		super(__class__, self).__init__(name, url_base, url_base_adv, numPerPage, flag, UtilRequest(False, False))

	def getUrl(self, adv, kwd, author):
		url = self.base_url
		if adv == 1:
			url = self.base_url_adv
			author = self.stripAuthor(author)
			url += self.url_fmt_type_a
			url += (self.url_fmt_title_a % kwd)
			url += (self.url_fmt_author % author)
		else:
			url += (self.url_fmt_title % kwd)
			url += self.url_fmt_type
		return url

	def getTotalNumBooks(self, url):
		# print("%s" % url)
		html = self.util_req.getHtmlByGet(url)
		return int(getTagValueWithHtml(html, self.path_num)[0].text)

	def getUrlPerPage(self, url, page):
		url = url + (self.url_fmt_page % page)
		return url

	def createBooks(self, url):
		html = self.util_req.getHtmlByGet(url)
		self.soup_books = getTagValueWithHtml(html, self.path_root)
		return len(self.soup_books)

	def setValues(self, _list, idx):
		# get values
		rec = self.soup_books[idx]

		title = getTagValue(rec, self.path_title).strip()
		# title = util_req.removeBAndGetValue(rec, self.path_title)
		author = self.getTagAuthor(rec, self.path_author)
		dec = getTagValue(rec, self.path_dec)
		publisher = getTagValue(rec, self.path_publisher)
		loc = getTagValue(rec, self.path_loc).strip()
		existence = getTagValue(rec, self.path_existence)
		return_date = ''
                if existence is not '':
		    return_date = getTagValue(rec, self.path_return)
		    existence += ', ' + return_date
		print("-- %s %s" % (loc, title))

		# set to cells
		_list.append(title)
		_list.append(author)
		_list.append(dec)
		_list.append(publisher)
		_list.append(loc)
		_list.append(existence)

    # private
	def getTagAuthor(self, soup, path):
		res = getTagValue(soup, path)
		if res.lower().startswith("by "):
			res = res.split(' ')[1]
		return res
