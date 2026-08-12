"""
광주시도서관 EUC-KR 및 JNET Type A/B 엔드포인트 탐색
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import urllib.parse
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

# 1. EUC-KR 인코딩 테스트
kwd_euckr = urllib.parse.quote("파이썬".encode("euc-kr"))
url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"

print(f"=== EUC-KR GET {url}?searchKeyword={kwd_euckr} ===")
r_euckr = session.get(f"{url}?searchType=SIMPLE&searchCategory=ALL&searchKey=ALL&searchLibrary=ALL&searchKeyword={kwd_euckr}", headers=HEADERS, timeout=10, verify=False)
print("Status:", r_euckr.status_code, "Len:", len(r_euckr.text), "파이썬 count:", r_euckr.text.count("파이썬"))

# 2. 광주시 다른 메뉴 엔드포인트 탐색
menu_urls = [
    "https://lib.gjcity.go.kr/intro/menu/10035/program/30005/searchResultList.do",
    "https://lib.gjcity.go.kr/lay1/program/S1T1C2/jnet/resourcessearch/resultList.do",
    "https://lib.gjcity.go.kr/search/resultList.do"
]

for murl in menu_urls:
    print(f"\n=== GET {murl} ===")
    try:
        r = session.get(murl, params={"searchKeyword": "파이썬", "searchType": "SIMPLE"}, headers=HEADERS, timeout=8, verify=False)
        print(f"Status: {r.status_code}, Len: {len(r.text)}, 파이썬: {r.text.count('파이썬')}")
        if r.status_code == 200 and r.text.count('파이썬') > 1:
            print("  FOUND GWANGJU MENU RESULTS!")
    except Exception as e:
        print(f"Error: {e}")
