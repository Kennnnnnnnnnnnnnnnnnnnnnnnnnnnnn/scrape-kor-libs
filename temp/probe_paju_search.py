"""
파주시도서관 통합검색(plusSearchResultList.do) GET 실시간 검증
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
    'Referer': 'https://lib.paju.go.kr/intro/index.do'
}

# 1. 1차 메인페이지 방문 (세션 쿠키 및 csSignature 획득)
main_url = "https://lib.paju.go.kr/intro/index.do"
try:
    print("=== 1. 파주시 메인페이지 방문 ===")
    r_main = session.get(main_url, headers=HEADERS, timeout=8, verify=False)
    soup_main = BeautifulSoup(r_main.text, "html.parser")
    
    sig_tag = soup_main.select_one("form#topSearchForm input[name='csSignature']")
    sig = sig_tag.get("value") if sig_tag else ""
    print("  Acquired Cookies:", session.cookies.get_dict())
    print("  Acquired csSignature:", sig)
    
    # 2. 획득한 세션을 그대로 연동하여 통합 검색 수행!
    search_url = "https://lib.paju.go.kr/jalib/plusSearchResultList.do"
    params = {
        "csSignature": sig,
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchLibrary": "ALL",
        "searchKey": "ALL",
        "searchKeyword": "파이썬"
    }
    
    print("\n=== 2. 통합 검색 요청 ===")
    r_search = session.get(search_url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("  Search Status:", r_search.status_code)
    print("  Search HTML Length:", len(r_search.text))
    
    with open("paju_result.html", "w", encoding="utf-8") as f:
        f.write(r_search.text)
    print("  Saved paju_result.html")
    
    # 3. 책 목록 존재 여부 탐색
    soup_search = BeautifulSoup(r_search.text, "html.parser")
    titles = soup_search.select(".title a, a[href*='Detail'], .book_list a, a.book_name")
    print(f"  Titles found: {len(titles)}")
    for idx, t in enumerate(titles[:5]):
        print(f"    [{idx}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
except Exception as e:
    print("Error:", e)
