"""
의왕시도서관 검색어 파라미터 변형 테스트
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
    'Referer': 'https://www.uwlib.or.kr/intro/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# 메인 페이지 먼저 방문 (세션 쿠키 획득)
session.get("https://www.uwlib.or.kr/intro/index.do", headers=HEADERS, timeout=8, verify=False)

url = "https://www.uwlib.or.kr/jungang/program/searchResultList.do"

# POST 방식 다양한 조합 테스트
variants = [
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchField": "ALL", "searchWord": "파이썬", "searchLibrary": "ALL"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchField": "ALL", "searchWord": "파이썬", "searchLibrary": "ALL", "searchPbLibrary": "ALL", "searchSmLibrary": "ALL"},
    {"searchType": "SIMPLE", "searchMenuCategory": "ALL", "searchCategory": "ALL", "searchField": "ALL", "searchWord": "파이썬"},
]

for vi, payload in enumerate(variants):
    print(f"\n=== Variant {vi} ===")
    r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    no_result = soup.select_one("li.noResultNote")
    cnt = r.text.count("파이썬")
    book_items = soup.select("li.resultItem, li.searchResultItem, ul.listWrap > li:not(.noResultNote)")
    print(f"  Status: {r.status_code}, Length: {len(r.text)}, 파이썬 count: {cnt}")
    print(f"  No result: {'Yes' if no_result else 'No'}, Items: {len(book_items)}")

# GET 방식 테스트
print(f"\n=== GET 방식 ===")
params = {"searchType": "SIMPLE", "searchCategory": "ALL", "searchField": "ALL", "searchWord": "파이썬", "searchLibrary": "ALL"}
r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")
no_result = soup.select_one("li.noResultNote")
book_items = soup.select("ul.listWrap > li:not(.noResultNote)")
print(f"  Status: {r.status_code}, Length: {len(r.text)}, Items: {len(book_items)}, No result: {'Yes' if no_result else 'No'}")

# 간단한 GET 키워드
params2 = {"searchWord": "파이썬"}
r2 = session.get(url, params=params2, headers=HEADERS, timeout=12, verify=False)
soup2 = BeautifulSoup(r2.text, "html.parser")
no_result2 = soup2.select_one("li.noResultNote")
book_items2 = soup2.select("ul.listWrap > li:not(.noResultNote)")
print(f"  Simple GET -> Status: {r2.status_code}, Length: {len(r2.text)}, Items: {len(book_items2)}, No result: {'Yes' if no_result2 else 'No'}")
