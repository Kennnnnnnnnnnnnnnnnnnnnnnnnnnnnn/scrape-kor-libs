"""
경기도 광주시도서관 (lib.gjcity.go.kr) JNET 상세검색 분석
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import re
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
    'Referer': 'https://lib.gjcity.go.kr/'
}

print("=== 1. 광주시도서관 메인 접속 및 Cookie 세션 형성 ===")
r_main = session.get("https://lib.gjcity.go.kr/", headers=HEADERS, timeout=10, verify=False)
print("Main status:", r_main.status_code)

# 검색 페이지 렌더링 확인
search_page_url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
r_page = session.get(search_page_url, headers=HEADERS, timeout=10, verify=False)
print("Search page status:", r_page.status_code)

soup = BeautifulSoup(r_page.text, "html.parser")
forms = soup.select("form")
print(f"Forms on search page: {len(forms)}")
for i, form in enumerate(forms):
    print(f"  Form[{i}] action='{form.get('action')}' id='{form.get('id')}'")
    for inp in form.select("input")[:15]:
        print(f"    input: name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")

# 다양한 POST / GET 파라미터 테스트
test_params = [
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL", "searchKeyword": "파이썬"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "TITLE", "searchLibrary": "ALL", "searchKeyword": "파이썬"},
    {"searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchKeyword": "파이썬", "searchWord": "파이썬"},
]

print("\n=== 2. POST 요청 테스트 ===")
for p in test_params:
    r_post = session.post(search_page_url, data=p, headers=HEADERS, timeout=10, verify=False)
    cnt = r_post.text.count("파이썬")
    book_dl = BeautifulSoup(r_post.text, "html.parser").select("dl.bookDataWrap, li.resultListItem, tr.resultListItem")
    print(f"  POST params={p['searchKey']} -> Status: {r_post.status_code}, Len: {len(r_post.text)}, 파이썬: {cnt}, items: {len(book_dl)}")
    if cnt > 1 and len(book_dl) > 0:
        with open("gwangju_success.html", "w", encoding="utf-8") as f:
            f.write(r_post.text)
        print("  FOUND GWANGJU RESULTS!")
