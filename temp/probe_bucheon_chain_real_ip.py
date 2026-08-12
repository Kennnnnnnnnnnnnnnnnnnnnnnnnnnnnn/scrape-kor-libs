"""
부천시 https://alpasq.bcl.go.kr/search/keyword/파이썬 직접 접속 검증
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://alpasq.bcl.go.kr/search/keyword/" + urllib.parse.quote("파이썬")

print(f"=== GET {url} ===")
r = session.get(url, headers=HEADERS, timeout=12, verify=False, allow_redirects=True)
print("Status:", r.status_code)
print("Final URL:", r.url)
print("Length:", len(r.text))
print("'파이썬' count:", r.text.count("파이썬"))

if r.status_code == 200:
    with open("bucheon_keyword_search_result.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved bucheon_keyword_search_result.html")

    soup = BeautifulSoup(r.text, "html.parser")
    print("Items found:")
    for sel in ["dl.bookDataWrap", "div.resultItem", "li.resultListItem", "tr.resultListItem", "table tbody tr", "ul.listWrap > li", "div.book_info", "div.search_list li"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
