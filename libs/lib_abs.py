from abc import *

BIT_LIB_FLAG_IGNORE_EXISTENCE = 0b1


def quirk_existence(existence, flag):
	if flag & BIT_LIB_FLAG_IGNORE_EXISTENCE:
		existence = ''
	return existence

class libAbs(metaclass=ABCMeta):
	@abstractmethod
	def create(self, _list, val, flag):
		pass

	def __init__(self, name, url, url_adv, num_per_page, flag, util_req):
		self.name = name
		self.base_url = url
		self.base_url_adv = url_adv
		self.num_per_page = num_per_page
		self.list_black_prefix = None
		self.list_black_in = None
		self.flag = flag
		self.util_req = util_req

	def __del__(self):
		del self.util_req

	def addBlacks(self, list_prefix, list_in):
		self.list_black_prefix = list_prefix
		self.list_black_in = list_in

	def checkTitle(self, val):
		for item in self.list_black_prefix:
			if val.startswith(item):
				print("Title should not begin with %s: %s" % (item, val))
				return 1
		for item in self.list_black_in:
			if item in val:
				print("-- Title should not include %s: %s" % (item, val))
				return 1
		return 0

	@abstractmethod
	def getUrl(self, adv, kwd, author):
		pass

	@abstractmethod
	def getTotalNumBooks(self, url):
		pass

	@abstractmethod
	def getUrlPerPage(self, url, page):
		pass

	@abstractmethod
	def createBooks(self, url):
		pass

	@abstractmethod
	def setValues(self, _list, idx):
		pass

	def stripAuthor(self, val):
		#print("11 %s" % val)
		if val.find(';'):
			val = val.split(';')[0]
		#print("22 %s" % val)
		if val.find(' by '):
			arr = val.split('by ')
			if len(arr) == 1:
				val = arr[0]
			else:
				val = arr[1]
		#print("33 %s" % val)
		val = val.split(' ')[0]
		return val
