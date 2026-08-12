"""
안성시도서관 통합검색 Search.jsp 엔드포인트 테스트
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import sys

sys.stdout.reconfigure(encoding='utf-8')
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
    'Referer': 'https://www.anseong.go.kr/library/main.do'
}

url = "https://www.anseong.go.kr/search/front/Search.jsp"
params = {
    "searchKey": "all",
    "qt": "파이썬"
}

print(f"=== GET {url} ===")
r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
print(f"Status: {r.status_code}, Length: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")

if r.status_code == 200:
    with open("anseong_search_jsp.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved anseong_search_jsp.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    # 주요 구조 파싱
    for sel in ["div.result", "li", "tr", "div.book_info", "div.list", "dt"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
