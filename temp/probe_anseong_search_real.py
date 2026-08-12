"""
안성시도서관 진짜 검색 서블릿(search.do) GET 실시간 검증
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
    'Referer': 'https://www.anseong.go.kr/library/contents.do?mId=0101010000'
}

# 안성 진짜 검색 서블릿
url = "https://www.anseong.go.kr/library/search/search.do"
params = {
    "mId": "0101010100",
    "searchKeyType": "K",
    "page": "1",
    "searchType": "ALL",
    "searchTxt": "파이썬",
    "branchId": ""
}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("anseong_real_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved anseong_real_result.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    titles = soup.select("a[href*='searchView.do'], a.title, .book-title a, a[onclick*='View']")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
