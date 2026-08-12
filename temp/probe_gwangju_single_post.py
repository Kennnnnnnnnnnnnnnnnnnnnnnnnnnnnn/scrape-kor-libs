"""
광주시도서관 JNET POST 세션 분리 검증
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Origin': 'https://lib.gjcity.go.kr',
    'Referer': 'https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do'
}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

# 1단계: 세션 생성 없이 단일 POST 직접 제출
r1 = session.post(url, data=payload, headers=headers, timeout=12, verify=False)
print("Single POST Status:", r1.status_code, "Len:", len(r1.text), "파이썬 count:", r1.text.count("파이썬"))

if r1.text.count("파이썬") > 0:
    soup = BeautifulSoup(r1.text, "html.parser")
    items = soup.select("dl.bookDataWrap")
    print(f"  ★ GWANGJU SINGLE POST SUCCESS! items count: {len(items)} ★")
    for i, item in enumerate(items[:3]):
        title_tag = item.select_one("dt.tit a")
        print(f"    [{i+1}] {title_tag.text.strip() if title_tag else 'None'}")
