"""
연천군도서관 CSRF 토큰 획득 및 POST 검색 실시간 검증
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
    'Referer': 'https://library.yeoncheon.go.kr/'
}

try:
    # 1. 1차 간략검색 인덱스 페이지 접속 (CSRF 토큰 및 쿠키 세션 획득)
    print("=== 1. 간략검색 페이지 접속 ===")
    r_simple = session.get("https://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do", headers=HEADERS, timeout=10, verify=False)
    print("  Status:", r_simple.status_code)
    
    soup_simple = BeautifulSoup(r_simple.text, "html.parser")
    csrf_tag = soup_simple.select_one("input[name='_csrf']")
    csrf_val = csrf_tag.get("value") if csrf_tag else "None"
    print("  Acquired CSRF:", csrf_val)
    print("  Cookies:", session.cookies.get_dict())
    
    # 2. CSRF 토큰을 동봉하여 POST 방식으로 자료 검색 요청!
    url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"
    payload = {
        "_csrf": csrf_val,
        "searchType": "SIMPLE",
        "searchLibrary": "ALL",
        "searchCategory": "ALL",
        "searchField": "ALL",
        "searchWord": "파이썬"
    }
    
    print("\n=== 2. CSRF 동봉 POST 검색 요청 ===")
    r_search = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
    print("  Search Status:", r_search.status_code)
    print("  Search HTML Length:", len(r_search.text))
    
    with open("yeoncheon_real_search_result.html", "w", encoding="utf-8") as f:
        f.write(r_search.text)
    print("  Saved yeoncheon_real_search_result.html")
    
    soup_result = BeautifulSoup(r_search.text, "html.parser")
    
    # 책 제목 태그 분석
    titles = soup_result.select(".title a, a[href*='Detail'], .book_list a, a.book_name, dt.tit a, tr.book_list td a, .book-title a")
    print(f"  Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"    [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    print("  Keyword count in text:", r_search.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
