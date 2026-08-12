"""
가평군도서관 지점코드 및 검색어 필드 보완 통합검색 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('http://', SslAdapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'http://www.gaplib.go.kr/intro/menu/10035/program/30005/searchSimple.do'
}

url = "http://www.gaplib.go.kr/intro/menu/10035/program/30005/searchResultList.do"

# 다중 지점 및 파라미터 조합
params = [
    ("searchLibraryArr", "MA"),
    ("searchLibraryArr", "MC"),
    ("searchLibraryArr", "MD"),
    ("searchLibraryArr", "MB"),
    ("searchKeyword", "파이썬"),
    ("mainSearchKeyword", "파이썬"),
    ("searchType", "SIMPLE"),
    ("searchCategory", "ALL"),
    ("searchKey", "ALL")
]

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gapyeong_real_library_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved gapyeong_real_library_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items: {len(book_items)}")
    for i, item in enumerate(book_items[:5]):
        title_tag = item.select_one("dt.tit a")
        title = title_tag.text.strip() if title_tag else "None"
        author_tag = item.select_one("dd.author span")
        author = author_tag.text.strip() if author_tag else "None"
        call_tag = item.select_one("dd.data span")
        call_no = call_tag.text.strip() if call_tag else "None"
        print(f"  [{i}] Title: {title} | Author: {author} | CallNo: {call_no}")
        
except Exception as e:
    print("Error:", e)
