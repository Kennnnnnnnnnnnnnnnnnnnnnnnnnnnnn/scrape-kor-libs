"""
의정부시 도서관(uilib.net) SSL 암호화 수준 강하를 적용한 검색 진단
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3

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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

CANDIDATES = [
    "https://www.uilib.net/search/searchResultList.do",
    "https://www.uilib.net/intro/searchResultList.do",
    "https://www.uilib.net/intro/program/plusSearchResultList.do",
    "https://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do",
    "https://www.uilib.net/intro/menu/10041/program/30001/plusSearchResultList.do"
]

params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

for url in CANDIDATES:
    print(f"\nURL: {url}")
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
        print(f"  Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 4000:
            soup = BeautifulSoup(r.text, "html.parser")
            total_tag = soup.select_one("#totalCnt, .totalCnt, .search_total")
            total = total_tag.text.strip() if total_tag else "No totalCnt"
            print(f"    [SUCCESS!!!] Total: {total}")
            
            titles = soup.select("a.book_name, .bookArea a.book_name, .title a, a[href*='plusSearchDetail']")
            print(f"    Titles found: {len(titles)}")
            for i, t in enumerate(titles[:5]):
                print(f"      [{i}] Title: {t.text.strip()}")
                
    except Exception as e:
        print(f"  Error: {e}")
