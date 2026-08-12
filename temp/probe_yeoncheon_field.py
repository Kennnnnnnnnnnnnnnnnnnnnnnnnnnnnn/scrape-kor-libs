"""
연천군도서관 searchKeyword 필드 매핑 통합검색 실시간 검증
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
    'Referer': 'https://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"

# 1. POST 검증
payload_post = {
    "searchType": "SIMPLE",
    "searchLibrary": "ALL",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchKeyword": "파이썬"  # searchWord 가 아닌 searchKeyword 명시!
}

# 2. GET 검증
params_get = {
    "searchType": "SIMPLE",
    "searchLibrary": "ALL",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchKeyword": "파이썬"
}

try:
    print("=== 1. POST 방식 검증 ===")
    r_post = session.post(url, data=payload_post, headers=HEADERS, timeout=12, verify=False)
    print("  POST Status:", r_post.status_code)
    print("  POST HTML Length:", len(r_post.text))
    
    print("\n=== 2. GET 방식 검증 ===")
    r_get = session.get(url, params=params_get, headers=HEADERS, timeout=12, verify=False)
    print("  GET Status:", r_get.status_code)
    print("  GET HTML Length:", len(r_get.text))
    
    if r_post.status_code == 200 and len(r_post.text) > 1000:
        with open("yeoncheon_real_search_ok.html", "w", encoding="utf-8") as f:
            f.write(r_post.text)
        print("\nSaved yeoncheon_real_search_ok.html")
        
        soup = BeautifulSoup(r_post.text, "html.parser")
        titles = soup.select(".title a, a[href*='Detail'], .book_list a, a.book_name, dt.tit a, tr.book_list td a, .book-title a")
        print(f"  Titles found: {len(titles)}")
        for i, t in enumerate(titles[:5]):
            print(f"    [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
            
except Exception as e:
    print("Error:", e)
