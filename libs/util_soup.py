from bs4 import BeautifulSoup
import sys

idx_fmt_cell = '%s%d'
def getCellIdx(col, row):
    return idx_fmt_cell % (col, row)

def getSoup(html):
	return BeautifulSoup(html, "html5lib")

def getTagValueWithHtml(html, path):
    soup = BeautifulSoup(html, "html5lib")
    '''
    arr = soup.select('#searchForm')
    print(arr[0].text)
    sys.exit(3)
    '''
    arr = soup.select(path)
    return arr

def getTagValueWithHtml_a(html, path):
    soup = BeautifulSoup(html, "html.parser")
    arr = soup.select(path)
    return arr

def getTagProp(soup, path, key):
    res = ''
    arr = soup.select(path)
    if len(arr) > 0:
        res = arr[0][key]
    return res

def getTagValue(soup, path):
    res = ''
    arr = soup.select(path)
    if len(arr) > 0:
        res = arr[0].text
    return res

def removeBAndGetValue(soup, path):
    html = soup.select(path)[0].text
    soup = BeautifulSoup(html, "html5lib")
    res = ''
    '''
    soup_a = soup.b.decompose()
    res = soup_a[0].text
    arr = soup.select(path)
    if len(arr) > 0:
        res = arr[0].text
    '''
    return res