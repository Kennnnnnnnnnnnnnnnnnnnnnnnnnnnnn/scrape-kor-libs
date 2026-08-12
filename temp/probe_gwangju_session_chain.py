"""
경기도 광주시도서관 (lib.gjcity.go.kr) 모든 파라미터 조합 Fuzzing
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
    'Referer': 'https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do'
}

# 1. 세션 생성
session.get("https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do", headers=HEADERS, timeout=10, verify=False)

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"

# 파라미터 조합
payloads = [
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL"},
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "BOOK", "searchKey": "ALL", "searchLibrary": "ALL"},
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "TITLE", "searchLibrary": "ALL"},
    {"q": "파이썬", "searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL"},
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "MA"},
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibraryArr": "MA"},
]

print("=== POST Fuzzing ===")
for i, p in enumerate(payloads):
    try:
        r = session.post(url, data=p, headers=HEADERS, timeout=10, verify=False)
        cnt = r.text.count("파이썬")
        print(f"[{i}] POST -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {cnt}")
        if cnt > 1:
            print("  ★ GWANGJU POST MATCH ★")
            with open(f"gwangju_match_post_{i}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
    except Exception as e:
        print(f"[{i}] Error: {e}")

print("\n=== GET Fuzzing ===")
for i, p in enumerate(payloads):
    try:
        r = session.get(url, params=p, headers=HEADERS, timeout=10, verify=False)
        cnt = r.text.count("파이썬")
        print(f"[{i}] GET -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {cnt}")
        if cnt > 1:
            print("  ★ GWANGJU GET MATCH ★")
            with open(f"gwangju_match_get_{i}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
    except Exception as e:
        print(f"[{i}] Error: {e}")
