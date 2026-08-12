"""
연천군도서관 진짜 검색 서블릿(searchList.do) GET 실시간 검증
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
session.mount('https://', SslAdapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do'
}

url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchList.do"

# 다중 진짜 지점코드와 searchKeyword 조립
params = [
    ("searchLibraryArr", "MA"),
    ("searchLibraryArr", "BR"),
    ("searchLibraryArr", "ME"),
    ("searchLibraryArr", "MD"),
    ("searchLibraryArr", "MF"),
    ("searchLibraryArr", "MG"),
    ("searchKeyword", "파이썬"),
    ("searchType", "SIMPLE"),
    ("searchLibrary", "ALL"),
    ("searchKey", "ALL")
]

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yeoncheon_real_ok.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yeoncheon_real_ok.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 목록 파싱 (보통 JNET 표준은 dl.bookDataWrap, dt.tit a 사용)
    book_items = soup.select("dl.bookDataWrap, div.bookData, tr.book_list")
    print(f"Book items count: {len(book_items)}")
    for i, item in enumerate(book_items[:3]):
        title_tag = item.select_one("dt.tit a, div.book_name a, td.title a")
        title = title_tag.text.strip() if title_tag else "None"
        print(f"  [{i}] Title: {title}")
        
except Exception as e:
    print("Error:", e)
