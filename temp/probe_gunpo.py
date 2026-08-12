"""
군포시도서관(gunpolib.go.kr) 통합검색 분석 스크립트
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
session.mount('http://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 메인 접속
print("=== 1. 군포시도서관 메인 접속 ===")
try:
    r = session.get("https://www.gunpolib.go.kr", headers=HEADERS, timeout=8, verify=False)
    print("  Status:", r.status_code)
    print("  URL:", r.url)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 폼 분석
    forms = soup.select("form")
    print(f"  Forms count: {len(forms)}")
    for i, form in enumerate(forms[:5]):
        print(f"    Form[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
        for inp in form.select("input")[:10]:
            print(f"      name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
except Exception as e:
    print("  Error:", e)

# 2. 대표적인 jnet / kolaseek 엔드포인트 테스트
print("\n=== 2. 엔드포인트 테스트 ===")
test_urls = [
    "https://www.gunpolib.go.kr/search/searchResultList.do",
    "https://www.gunpolib.go.kr/kolaseek/search/searchResultList.do",
    "https://www.gunpolib.go.kr/lay1/program/S1T1C2/jnet/resourcessearch/resultList.do"
]

for url in test_urls:
    params = {
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchKey": "ALL",
        "searchLibrary": "ALL",
        "searchKeyword": "파이썬"
    }
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  {url} -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print(f"    '파이썬' count: {r.text.count('파이썬')}")
    except Exception as e:
        print(f"  {url} -> Error: {e}")
