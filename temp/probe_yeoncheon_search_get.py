"""
연천군도서관 통합검색(searchResultList.do) GET 실시간 검증
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

url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"
params = {
    "searchType": "SIMPLE",
    "searchLibrary": "ALL",
    "searchCategory": "ALL",
    "searchField": "ALL",
    "searchWord": "파이썬"
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yeoncheon_result_get.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yeoncheon_result_get.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 목록 파싱
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select(".title a, a[href*='Detail'], .book_list a, a.book_name, dt.tit a, tr.book_list td a, .book-title a")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    print("Keyword count in text:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
