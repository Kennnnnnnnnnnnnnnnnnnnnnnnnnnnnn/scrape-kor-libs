from .lib_abs import *
from .util_soup import *
from .util_requests import *

dict_libs = {
'용인중앙도서관': {'subdm':'yongin','menuid':10181, 'subdm1':'MA'},
'구갈희망누리도서관': {'subdm':'gugal','menuid':10374, 'subdm1':'MI'},
'구성도서관': {'subdm':'guseong','menuid':10562, 'subdm1':'MD'},
'기흥도서관': {'subdm':'giheung','menuid':10758, 'subdm1':'MK'},
'남사도서관': {'subdm':'namsa','menuid':10955, 'subdm1':'MY'},
'동백도서관': {'subdm':'dongbaek','menuid':11147, 'subdm1':'MF'},
'모현도서관': {'subdm':'mohyeon','menuid':11343, 'subdm1':'ML'},
'보라도서관': {'subdm':'bora','menuid':11536, 'subdm1':'MM'},
'상현도서관': {'subdm':'sanghyeon','menuid':11731, 'subdm1':'MO'},
'서농도서관': {'subdm':'seonong','menuid':11928, 'subdm1':'MZ'},
'성복도서관': {'subdm':'seongbok','menuid':12123, 'subdm1':'NB'},
'수지도서관': {'subdm':'suji','menuid':12326, 'subdm1':'MB'},
'양지해밀도서관': {'subdm':'haemil','menuid':12537, 'subdm1':'MJ'},
'영덕도서관': {'subdm':'yeongdeok','menuid':12725, 'subdm1':'NN'},
'이동꿈틀도서관': {'subdm':'idong','menuid':12917, 'subdm1':'NX'},
'죽전도서관': {'subdm':'jukjeon','menuid':13108, 'subdm1':'ME'},
'청덕도서관': {'subdm':'cheongdeok','menuid':13304, 'subdm1':'MP'},
'포곡도서관': {'subdm':'pogok','menuid':13496, 'subdm1':'MC'},
'흥덕도서관': {'subdm':'heungdeok','menuid':13691, 'subdm1':'MN'},
}

class libYongin(libAbs):
	area_name = '용인'

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
			subdm1 = dict_libs[val]['subdm1']
			url_base = "https://lib.yongin.go.kr/%s/menu/%d/program/30012/plusSearchResultList.do?searchCategory=BOOK&searchKey=TITLE&searchLibraryArr=%s&searchOrder=DESC" % \
					   (subdm, menuid, subdm1)
			obj = libYongin(val, url_base, url_base, flag)
			_list.append(obj)
		return obj

	def __init__(self, name, url_base, url_base_adv, flag):
		numPerPage = 20
		self.url_fmt_num = "&searchRecordCount=%d" % numPerPage
		self.url_fmt_type = "&searchType=SIMPLE"
		self.url_fmt_type_a = "&searchType=DETAIL"
		self.url_fmt_page = "&currentPageNo=%d"
		self.url_fmt_title = "&searchKeyword=%s"
		self.url_fmt_title_a = "&searchKey1=TITLE&searchKeyword1=%s&searchOperator1=AND"
		self.url_fmt_author = "&searchKey2=AUTHOR&searchKeyword2=%s&searchOperator2=AND"

		# <strong class="highlight">11</strong>
		self.path_num = "#searchForm > div > div:nth-of-type(3) > div > div > strong:nth-of-type(2)"
		#self.path_num = "#contentArea"

		# <div id="bookList">
		self.path_root = "#searchForm > div > div:nth-of-type(3) > div:nth-of-type(2) > ul > li"
		path_aux = "div > div > div:nth-of-type(1)"

		# self.path_title = path_aux + " > div:nth-of-type(1) > a > b"
		self.path_title = path_aux + " > div:nth-of-type(1) > a"
		self.path_author = path_aux + " > div:nth-of-type(2) > 	div > p"
		self.path_publisher = path_aux + " > div:nth-of-type(3) > div > p:nth-of-type(1)"
		self.path_dec = path_aux + " > div:nth-of-type(3) > div > p:nth-of-type(3)"
		self.path_loc = path_aux + " > div:nth-of-type(4) > div:nth-of-type(1) > p:nth-of-type(2)"
		self.path_existence = "li > div > div > div:nth-of-type(2)" + " > div > p"
		self.path_return = path_aux + " > div:nth-of-type(5) > div > p:nth-of-type(2)"

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
		return_date = getTagValue(rec, self.path_return)
		existence += ', ' + return_date
		existence = quirk_existence(existence, self.flag)
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
