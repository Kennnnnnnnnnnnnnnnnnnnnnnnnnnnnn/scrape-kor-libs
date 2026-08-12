"""
의왕시도서관 정확한 검색 URL (/intro/program/searchResultList.do) 실시간 검증
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
    'Referer': 'https://www.uwlib.or.kr/intro/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# 1. POST 방식으로 /intro/program/searchResultList.do
urls = [
    "https://www.uwlib.or.kr/intro/program/searchResultList.do",
    "https://www.uwlib.or.kr/jungang/program/searchResultList.do"
]

for url in urls:
    payload = {
        "searchType": "SIMPLE",
        "searchCategory": "ALL",
        "searchLibrary": "ALL",
        "searchField": "ALL",
        "searchWord": "파이썬"
    }
    
    print(f"\n=== POST {url} ===")
    try:
        r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        print(f"  '파이썬' count: {r.text.count('파이썬')}")
        print(f"  '청구기호' count: {r.text.count('청구기호')}")
        
        if r.text.count("파이썬") > 0:
            with open(f"uiwang_result_{url.split('/')[-2]}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"  Saved result HTML")
            
            soup = BeautifulSoup(r.text, "html.parser")
            
            # 결과 리스트 파싱
            items = soup.select("div.resultItem, div.bookData, dl.bookDataWrap, tr.resultListItem, li.resultItem")
            print(f"  Result items: {len(items)}")
            
            # 대체 구조
            tds = soup.select("table tr td a, div.bookListArea a, ul.resultList li a")
            print(f"  Alternative links: {len(tds)}")
            for i, td in enumerate(tds[:5]):
                print(f"    [{i}] {td.text.strip()[:50]}")
                
    except Exception as e:
        print(f"  Error: {e}")
