"""
광주시도서관 지연시간(sleep) 추가 단일 요청 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import time
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do'
}

print("1. 메인 페이지 세션 생성")
r1 = session.get("https://lib.gjcity.go.kr/", headers=HEADERS, timeout=10, verify=False)
print("Main status:", r1.status_code)

time.sleep(2.5)

print("2. 단일 검색 요청")
url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
params = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

r2 = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
print("Search status:", r2.status_code, "Len:", len(r2.text), "파이썬 count:", r2.text.count("파이썬"))

if r2.text.count("파이썬") > 0:
    with open("gwangju_clean_result.html", "w", encoding="utf-8") as f:
        f.write(r2.text)
    print("Saved gwangju_clean_result.html!")

    soup = BeautifulSoup(r2.text, "html.parser")
    # 항목 리스트 추출
    for sel in ["dl.bookDataWrap", "div.resultItem", "li.resultListItem", "tr.resultListItem", "table.resultList tr", "div.book_dataInner"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
