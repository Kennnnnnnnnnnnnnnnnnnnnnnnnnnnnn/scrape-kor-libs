"""
경기도 광주시도서관 GwangjuScraper 연동 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import time
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do'
}

# 메인 페이지 접속
session.get("https://lib.gjcity.go.kr/", headers=headers, timeout=8, verify=False)
time.sleep(1.0)

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

r = session.post(url, data=payload, headers=headers, timeout=12, verify=False)
print("Status:", r.status_code, "Length:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")
cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
print("Total count tag:", cnt_tag.text.strip() if cnt_tag else "None")

book_items = soup.select("dl.bookDataWrap, div.resultItem, li.resultListItem, tr.resultListItem")
print(f"Book items: {len(book_items)}")

for i, item in enumerate(book_items[:5]):
    title_tag = item.select_one("dt.tit a")
    title = title_tag.text.strip() if title_tag else "None"
    print(f"  [{i+1}] {title[:40]}")
