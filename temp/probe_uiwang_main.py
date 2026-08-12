"""
의왕시도서관(uwlib.or.kr) 통합검색 실시간 검증
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

# 1. 메인 접속 -> 검색 폼 구조 분석
print("=== 1. 메인 페이지 분석 ===")
try:
    r = session.get("http://www.uwlib.or.kr", headers=HEADERS, timeout=8, verify=False)
    print("  Status:", r.status_code)
    print("  URL:", r.url)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 검색 관련 링크 & 폼
    search_links = [a for a in soup.select("a") if a.get("href") and "search" in a.get("href", "").lower()]
    print(f"  Search links: {len(search_links)}")
    for j, a in enumerate(search_links[:10]):
        print(f"    [{j}] '{a.text.strip()[:30]}' -> {a.get('href')}")
    
    forms = soup.select("form")
    print(f"  Forms: {len(forms)}")
    for i, form in enumerate(forms[:5]):
        print(f"    Form[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
        for inp in form.select("input")[:10]:
            print(f"      name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
except Exception as e:
    print("  Error:", e)

# 2. 일반적인 JNET 패턴 테스트
print("\n=== 2. JNET 패턴 테스트 ===")
jnet_urls = [
    "http://www.uwlib.or.kr/jnet/resourcessearch/resultList.do",
    "http://www.uwlib.or.kr/search/resultList.do",
    "http://www.uwlib.or.kr/plusSearchResultList.do"
]
for test_url in jnet_urls:
    params = {
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchKey": "ALL",
        "searchLibrary": "ALL",
        "searchKeyword": "파이썬"
    }
    try:
        r = session.get(test_url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  {test_url} -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 5000:
            print(f"    '파이썬' count: {r.text.count('파이썬')}")
    except Exception as e:
        print(f"  {test_url} -> Error: {e}")
