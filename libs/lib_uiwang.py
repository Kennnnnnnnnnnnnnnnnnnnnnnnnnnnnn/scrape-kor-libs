from .lib_abs import *
from .util_soup import *
from .util_requests import *

dict_libs = {
'중앙': {'subdm':'MA'},
'내손': {'subdm':'MB'},
'글로벌': {'subdm':'MC'},
'포일어울림': {'subdm':'MJ'},
'오전빛고운': {'subdm':'MD'},
'부곡글고운': {'subdm':'ME'},
'내손책고운': {'subdm':'MF'},
'청계참고운': {'subdm':'MG'},
'청계숲고운': {'subdm':'MH'},
'숲속옹달샘': {'subdm':'NH'},
}

class libUiwang(libAbs):
	area_name = '의왕'

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

			url_base = "https://www.uwlib.or.kr/kolaseek/plus/search/plusSearchResultList.do?"
			url_base += "searchLibraryArr=%s" % subdm
			url_base += "&searchCategory=BOOK&searchKey=TITLE&searchOrder=DESC"

			obj = libUiwang(val, url_base, url_base, flag)
			_list.append(obj)
		return obj

	def __init__(self, name, url_base, url_base_adv, flag):
		numPerPage = 20
		self.url_fmt_num = "&searchDisplay=%d" % numPerPage
		self.url_fmt_type = "&searchType=SIMPLE"
		self.url_fmt_type_a = "&searchType=DETAIL"
		self.url_fmt_page = "&currentPageNo=%d"
		self.url_fmt_title = "&searchKeyword=%s"
		self.url_fmt_title_a = "&searchKey1=TITLE&searchKeyword1=%s&searchOperator1=AND"
		self.url_fmt_author = "&searchKey2=AUTHOR&searchKeyword2=%s&searchOperator2=AND"

		# <b class="themeFC">4건</b>
		self.path_num = "#searchForm > p > b"

		# <div id="bookList">
		self.path_root = "#searchForm > ul > li"
		# path_aux = "dl"

		self.path_title = "dl > dt > a"
		self.path_author = "dl > dd.author > span:nth-child(1)"
		self.path_publisher = "dl > dd.author > span:nth-child(2)"
		self.path_dec = "dl > dd.data > span:nth-child(2)"
		self.path_loc = "dl > dd.site > span:nth-child(2)"
		self.path_sound = "dl > dd.site > span:nth-child(3)"
		self.path_existence = "dl > div.bookStateBar.clearfix > p > b"
		self.path_return = "dl > div.bookStateBar.clearfix > p"

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
		text = getTagValueWithHtml(html, self.path_num)[0].text.strip("건")
		return int(text)

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
		sound = self.getTagValueForSound(rec, self.path_sound)
		loc = getTagValue(rec, self.path_loc).strip()
		existence = getTagValue(rec, self.path_existence)
		return_date = getTagValue(rec, self.path_return)
		existence += ', ' + return_date
		existence = quirk_existence(existence, self.flag)
		print("-- %s %s" % (loc, title))
		# print("-- %s " % (author))

		# set to cells
		_list.append(title)
		_list.append(author)
		_list.append(dec)
		_list.append(publisher)
		_list.append(sound)
		_list.append(loc)
		_list.append(existence)

    # private
	def getTagAuthor(self, soup, path):
		res = getTagValue(soup, path)
		if res.lower().startswith("by "):
			res = res.split(' ')[1]
		return res

	def getTagValueForSound(self, soup, path):
		res = ""
		text = getTagValue(soup, path)
		if "있음" in text:
			res = 'O'
		return res
