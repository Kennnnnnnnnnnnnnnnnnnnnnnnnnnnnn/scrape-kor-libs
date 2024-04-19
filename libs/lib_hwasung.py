from .lib_abs import *
from .util_soup import *
from .util_requests import *

dict_libs = {
'남양도서관': {'subdm':'nylib', 'menuid':10160, 'searchManageCodeArr':'MA'},
'태안도서관': {'subdm':'talib', 'menuid':10291, 'searchManageCodeArr':'MB'},
'삼괴도서관': {'subdm':'sglib', 'menuid':10422, 'searchManageCodeArr':'MC'},
'병점도서관': {'subdm':'bjlib', 'menuid':10553, 'searchManageCodeArr':'MD'},
'봉담도서관': {'subdm':'bdlib', 'menuid':10684, 'searchManageCodeArr':'MG'},
'동탄복합문화센터도서관': {'subdm':'dtlib', 'menuid':10815, 'searchManageCodeArr':'MK'},
'송산도서관': {'subdm':'sslib', 'menuid':10946, 'searchManageCodeArr':'ML'},
'정남도서관': {'subdm':'jnlib', 'menuid':11077, 'searchManageCodeArr':'MM'},
'진안도서관': {'subdm':'jalib', 'menuid':11208, 'searchManageCodeArr':'MO'},
'왕배푸른숲도서관': {'subdm':'wblib', 'menuid':12125, 'searchManageCodeArr':'MW'},
'노을빛도서관': {'subdm':'neblib', 'menuid':12387, 'searchManageCodeArr':'MX'},
'중앙이음터도서관': {'subdm':'iutlib', 'menuid':11339, 'searchManageCodeArr':'MP'},
'다원이음터도서관': {'subdm':'dwlib', 'menuid':11470, 'searchManageCodeArr':'MR'},
'송린이음터도서관': {'subdm':'srlib', 'menuid':11601, 'searchManageCodeArr':'MS'},
'목동이음터도서관': {'subdm':'mdlib', 'menuid':11732, 'searchManageCodeArr':'MI'},
'서연이음터도서관': {'subdm':'sylib', 'menuid':12256, 'searchManageCodeArr':'MY'},
'두빛나래어린이도서관': {'subdm':'dbnarae', 'menuid':11863, 'searchManageCodeArr':'MF'},
'둥지나래어린이도서관': {'subdm':'djnarae', 'menuid':11994, 'searchManageCodeArr':'MH'},
'달빛나래어린이도서관': {'subdm':'mlnarae', 'menuid':12932, 'searchManageCodeArr':'TB'},
'작은도서관': {'subdm':'small', 'menuid':10109, 'searchManageCodeArr':'MZ'},
}

class libHwasung(libAbs):
	area_name = '화성'

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
			menuid = dict_libs[val]['menuid']
			searchManageCodeArr = dict_libs[val]['searchManageCodeArr']
			url_base = "https://www.hscitylib.or.kr/%s/menu/%d/program/30001/searchResultList.do?searchManageCodeArr=%s&searchArticle=SCORE&searchOrder=ASC" % \
					   (subdm, menuid, searchManageCodeArr)
			obj = libHwasung(val, url_base, url_base, flag)
			_list.append(obj)
		return obj

	def __init__(self, name, url_base, url_base_adv, flag):
		numPerPage = 20
		self.url_fmt_num = "&searchDisplay=%d" % numPerPage
		self.url_fmt_type = "&searchType=SIMPLE"
		self.url_fmt_type_a = "&searchType=DETAIL"
		self.url_fmt_page = "&currentPageNo=%d"
		self.url_fmt_title = "&searchKeyword=%s"
		self.url_fmt_title_a = "&searchAdvTitle=%s"
		self.url_fmt_author = "&searchAdvAuthor=%s"

		# <span id="totalCnt">4</span>
		self.path_num = "#searchForm > div:nth-of-type(2) > div > div:nth-of-type(1) > div > span"

		# <div id="bookList">
		self.path_root = "#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li"

		# <div class="book_dataInner">
		path_aux = "div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1)"

		self.path_title = path_aux + " > p > a"
		self.path_author = path_aux + " > ul > li:nth-of-type(1) > span:nth-of-type(1)"
		self.path_publisher = path_aux + " > ul > li:nth-of-type(1) > span:nth-of-type(2)"
		self.path_dec = path_aux + " > ul > li:nth-of-type(3) > span:nth-of-type(1)"
		self.path_sound = path_aux + " > ul > li:nth-of-type(3) > span:nth-of-type(2)"
		self.path_loc = path_aux + " > ul > li:nth-of-type(4) > span"
		self.path_existence = path_aux + " > ul > li:nth-of-type(5) > span:nth-of-type(1)"
		self.path_return = path_aux + " > ul > li:nth-of-type(5) > span:nth-of-type(2)"

		self.soup_books = None

		super(__class__, self).__init__(name, url_base, url_base_adv, numPerPage, flag, UtilRequest(False, False))

	def getUrl(self, adv, kwd, author):
		url = self.base_url
		# quirk for Hwasung
		if self.name == '작은도서관':
			adv = 0
		if adv == 1:
			url = self.base_url_adv
			author = self.stripAuthor(author)
			url += self.url_fmt_type_a
			url += (self.url_fmt_title % kwd)
			url += (self.url_fmt_author % author)
		else:
			url += (self.url_fmt_title % kwd)
			url += self.url_fmt_type
		#print("** %s" % url) ###
		return url

	def getTotalNumBooks(self, url):
		# print("!! %s" % url) ###
		html = self.util_req.getHtmlByGet(url)
		if html == '':
			return 0
		else:
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

		title = getTagProp(rec, self.path_title, 'title')
		author = self.getTagAuthor(rec, self.path_author)
		author = self.stripAuthor(author)
		dec = getTagValue(rec, self.path_dec)
		publisher = getTagValue(rec, self.path_publisher)
		sound = self.getTagValueForSound(rec, self.path_sound)
		loc = getTagValue(rec, self.path_loc)
		existence = getTagValue(rec, self.path_existence)
		return_date = getTagValue(rec, self.path_return)
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