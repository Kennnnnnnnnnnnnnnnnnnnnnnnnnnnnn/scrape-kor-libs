from .lib_abs import *
from .util_soup import *
from .util_requests import *

import sys
from bs4 import BeautifulSoup

dict_libs = {
	'석수도서관': {'subdm': 'MA'},
	'만안도서관': {'subdm': 'MI'},
	'삼덕도서관': {'subdm': 'MH'},
	'박달도서관': {'subdm': 'ME'},
	'평촌도서관': {'subdm': 'MB'},
	'관양도서관': {'subdm': 'MG'},
	'비산도서관': {'subdm': 'MC'},
	'호계도서관': {'subdm': 'MD'},
	'어린이도서관': {'subdm': 'MJ'},
	'벌말도서관': {'subdm': 'MF'},
	'안양역스마트도서관': {'subdm': 'MK'},
	'동안구청스마트도서관': {'subdm': 'ML'},
	'범계스마트도서관': {'subdm': 'MM'},
	'인덕원역스마트도서관': {'subdm': 'MN'},
}

class libAnyang(libAbs):
	area_name = '안양'

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
			url_base = "https://lib.anyang.go.kr/intro/menu/10003/program/30001/searchResultList.do?searchType=SIMPLE&searchManageCodeArr=%s" % subdm
			url_base_adv = "https://lib.anyang.go.kr/intro/menu/10004/program/30002/searchResultList.do?searchType=DETAIL&searchManageCodeArr=%s" % subdm
			url_rest = '&viewType=LIST&searchPubFormCode=MO&currentPageNo=1&searchArticle=SCORE&searchOrder=ASC&reSearchYn=N&smallLibSearchYn=N&eBookSearchYn=N'
			obj = libAnyang(val, url_base + url_rest, url_base_adv + url_rest, flag)
			_list.append(obj)
		return obj

	def __init__(self, name, url_base, url_base_adv, flag):
		numPerPage = 20
		self.url_fmt_num = "&searchDisplay=%d" % numPerPage
		self.url_fmt_page = "&currentPageNo=%d"
		self.url_fmt_title = "&searchKeyword=%s"
		self.url_fmt_title_adv = "&searchAdvTitle=%s"
		self.url_fmt_author_adv = "&searchAdvAuthor=%s"
		self.url_fmt_rest_adv = "&searchAdvContentsType=ALL&searchAdvTextLang=ALL&searchAdvContentsTypeArr=단행본"

		# <span id="totalCnt">4</span>
		self.path_num = "#searchForm > div:nth-of-type(2) > div > div:nth-of-type(1) > div > span"

		# <div id="bookList">
		self.path_root = "#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li"

		# <div class="book_dataInner">
		path_aux = "div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1)"
		self.fmt_id_rest = '#collectionInfo%d'
		path_aux_a = "div:nth-of-type(2) > div:nth-of-type(1) > table > tbody > tr"

		# XPATH to click
		self.xpath_click = '//*[@class="btn_haveInfo"]'

		self.path_title = path_aux + " > a"
		self.path_author = path_aux + " > ul > li:nth-of-type(1)"
		self.path_publisher = path_aux + " > ul > li:nth-of-type(3)"

		self.path_dec = path_aux_a + " > td:nth-of-type(4)"
		self.path_sound = path_aux_a + " > td:nth-of-type(7)"
		self.path_loc = path_aux_a + " > td:nth-of-type(6)"
		self.path_existence = path_aux_a + " > td:nth-of-type(2)"
		self.path_return = path_aux_a + " > td:nth-of-type(3)"

		self.soup_books = None
		self.soup_books_a = None
		self.arr_click = None

		super(__class__, self).__init__(name, url_base, url_base_adv, numPerPage, flag, UtilRequest(True, True))

	def getUrl(self, adv, kwd, author):
		url = self.base_url
		# quirk for
		if self.name == '작은도서관':
			adv = 0
		if adv == 1:
			url = self.base_url_adv
			author = self.stripAuthor(author)
			url += (self.url_fmt_title_adv % kwd)
			url += (self.url_fmt_author_adv % author)
			url += self.url_fmt_rest_adv
		else:
			url += (self.url_fmt_title % kwd)
		#print("** %s" % url) ###
		return url

	def getTotalNumBooks(self, url):
		# print("!! %s" % url) ###
		html = self.util_req.getHtmlByGet(url)
		if html == '':
			return 0
		else:
			str_res = getTagValueWithHtml(html, self.path_num)[0].text.strip()
			# print("getTotalNumBooks %s" % str_res)
			return int(str_res)

	def getUrlPerPage(self, url, page):
		url = url + (self.url_fmt_page % page)
		return url

	def createBooks(self, url):
		html = self.util_req.getHtmlByGet(url)
		self.soup_books = getTagValueWithHtml(html, self.path_root)

		self.util_req.get_by_browser(url)
		self.arr_click = self.util_req.get_elems_by_get_xpath(url, self.xpath_click)
		# print("createBooks %d %d" % (len(self.soup_books), len(self.arr_click)))
		return len(self.soup_books)

	def setValues(self, _list, idx):
		# get values
		rec = self.soup_books[idx]

		title = getTagValue(rec, self.path_title)
		author = self.getTagAuthor(rec, self.path_author)
		author = self.stripAuthor(author)
		publisher = getTagValue(rec, self.path_publisher)
		if publisher.lower().startswith("발행처 :"):
			loc = publisher.split(':')[1].strip()

		self.arr_click[idx].click()
		html = self.util_req.get_html_from_browser('thisBook-libraryList')
		if html == '':
			_list.append('TIMED OUT')
			return
		rec_a = getTagValueWithHtml_a(html, self.fmt_id_rest % (idx + 1))[0]

		dec = getTagValue(rec_a, self.path_dec)
		sound = self.getTagValueForSound(rec_a, self.path_sound)
		loc = getTagValue(rec_a, self.path_loc)
		existence = getTagValue(rec_a, self.path_existence)
		return_date = getTagValue(rec_a, self.path_return)
		if existence != '':
			existence += ', ' + return_date
		existence = quirk_existence(existence, self.flag)

		print("-- %s %s" % (loc, title))

		# set to cells
		_list.append(title)
		_list.append(author)
		_list.append(dec)
		_list.append(publisher)
		_list.append(sound)
		_list.append(loc)
		_list.append(existence)

	# private
	def getTagValueForSound(self, soup, path):
		res = ""
		text = getTagValue(soup, path)
		if text == "부록있음":
			res = "O"
		return res

	def getTagAuthor(self, soup, path):
		res = getTagValue(soup, path)
		if res.lower().startswith("by "):
			res = res.split(' ')[1]
		if res.lower().startswith("[by]"):
			res = res.split(']')[1]
		return res