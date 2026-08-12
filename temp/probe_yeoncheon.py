"""
연천군 도서관(library.yeoncheon.go.kr) 메인 및 검색 파라미터 상세 분석
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
session.mount('http://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("=== 1. 연천군도서관 메인 접속 ===")
try:
    r = session.get("https://library.yeoncheon.go.kr/", headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code, "Final URL:", r.url)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 폼 출력
    forms = soup.select("form")
    print(f"Forms: {len(forms)}")
    for i, form in enumerate(forms):
        print(f"  Form[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
        for inp in form.select("input")[:15]:
            print(f"    input: name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
except Exception as e:
    print("Error:", e)

# 2. 다양한 엔드포인트 테스트 (POST & GET)
print("\n=== 2. 엔드포인트 테스트 ===")
endpoints = [
    "https://library.yeoncheon.go.kr/search/searchResultList.do",
    "https://library.yeoncheon.go.kr/lay1/program/S1T1C2/jnet/resourcessearch/resultList.do",
    "https://library.yeoncheon.go.kr/kolaseek/search/searchResultList.do"
]

for url in endpoints:
    params = {
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchKey": "ALL",
        "searchLibrary": "ALL",
        "searchKeyword": "파이썬"
    }
    print(f"\nGET {url}")
    try:
        r_get = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  GET Status: {r_get.status_code}, Len: {len(r_get.text)}, '파이썬' count: {r_get.text.count('파이썬')}")
    except Exception as e:
        print(f"  GET Error: {e}")

    print(f"POST {url}")
    try:
        r_post = session.post(url, data=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  POST Status: {r_post.status_code}, Len: {len(r_post.text)}, '파이썬' count: {r_post.text.count('파이썬')}")
    except Exception as e:
        print(f"  POST Error: {e}")
