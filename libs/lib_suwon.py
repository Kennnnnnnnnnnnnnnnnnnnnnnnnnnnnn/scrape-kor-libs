from .lib_abs import *
from .util_soup import *
from .util_requests import *

dict_libs = {
'선경도서관': {'subdm':'MA'},
'중앙도서관': {'subdm':'MB'},
'창룡도서관': {'subdm':'MV'},
'화서다산도서관': {'subdm':'SB'},
'호매실도서관': {'subdm':'MY'},
'서수원도서관': {'subdm':'MG'},
'한림도서관': {'subdm':'MU'},
'버드내도서관': {'subdm':'MW'},
'북수원도서관': {'subdm':'MH'},
'대추골도서관': {'subdm':'MT'},
'일월도서관': {'subdm':'MZ'},
'광교홍재도서관': {'subdm':'MX'},
'영통도서관': {'subdm':'MC'},
'태장마루도서관': {'subdm':'MI'},
'광교푸른숲도서관': {'subdm':'SC'},
'매여울도서관': {'subdm':'SD'},
'망포글빛도서관': {'subdm':'SE'},
'슬기샘도서관': {'subdm':'MD'},
'지혜샘도서관': {'subdm':'MF'},
'바른샘도서관': {'subdm':'ME'},
'한아름도서관': {'subdm':'MK'},
'사랑샘도서관': {'subdm':'MN'},
'희망샘도서관': {'subdm':'MO'},
'반달어린이도서관': {'subdm':'MM'},
'화홍어린이도서관': {'subdm':'MP'},
}

class libSuwon(libAbs):
	area_name = '수원'
	def __init__(self, name, subdm, flag):
		self.fmt_url = "https://www.suwonlib.go.kr:8443/api/search"
		self.subdm = subdm
		self.kwd = ''
		self.author = ''
		self.page = 1
		self.dict_data = None

		numPerPage = 20

		super(__class__, self).__init__(name, self.fmt_url, self.fmt_url, numPerPage, flag, UtilRequest(False, False))

	@staticmethod
	def create(_list, val, flag):
		try:
			if dict_libs[val]:
				pass
		except KeyError:
			print("%s doesn't exist" % val)
		else:
			obj = libSuwon(val, dict_libs[val]['subdm'], flag)
			_list.append(obj)
		return obj

	def getUrl(self, adv, kwd, author):
		url = self.base_url
		if adv == 1:
			url = self.base_url_adv
			author = self.stripAuthor(author)
		self.kwd = kwd
		self.author = author
		#print("** %s" % url) ###
		return url

	def getTotalNumBooks(self, url):
		res = 0
		dict_data = self.submit(url)
		if dict_data is not None:
			res = dict_data['contents']['contentsTypeList'][0]['contentsTypeCount']
		return res

	def getUrlPerPage(self, url, page):
		self.page = page
		return url

	def createBooks(self, url):
		res = 0
		self.dict_data = self.submit(url)
		if self.dict_data is not None:
			res = len(self.dict_data['contents']['bookList'])
		return res

	def setValues(self, _list, idx):
        # get values
		rec = self.dict_data['contents']['bookList'][idx]
		title = rec['title']
		'''
		print(title)
		soup = getSoup(title)
		soup = getSoup(title)
			text = getTagValue(soup, 'span')
			soup.span.decompose()
			title = text + soup.text
		'''
		author = rec['author']

		dec = rec['callNo']
		publisher = rec['publisher']
		sound = self.getTagValueForSound(rec['bookAppendixFlag'])
		loc = rec['shelfLocName']
		existence = rec['loanStatus']
		return_date = rec['returnPlanDate']
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
	def submit(self, url):
		val = self.kwd
		if self.author != '':
			val += ' ' + self.author
		payload = {
			"searchKeyword": ("%s" % val),
			"pubFormCode": "MO",
			"page": ("%d" % self.page),
			"display": ("%d" % self.num_per_page),
			"article": "SCORE",
			"order": "DESC",
			"manageCode": ("%s" % self.subdm)
		}
		return self.util_req.getHtmlByPost(url, payload)

	def getTagValueForSound(self, text):
		res = ''
		if text == "부록있음":
			res = 'O'
		return res
