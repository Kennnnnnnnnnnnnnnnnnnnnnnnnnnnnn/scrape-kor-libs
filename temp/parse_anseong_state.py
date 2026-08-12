"""
안성시 book-state 내부 구조 확인
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
    'Referer': 'https://www.anseong.go.kr/library/main.do'
}

session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)

url = "https://www.anseong.go.kr/library/search/search.do?mId=0101010100"
payload = {
    "searchKeyType": "K",
    "searchTxt": "파이썬"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

dls = soup.select("div.anseong-search-list-table dl")

for i, dl in enumerate(dls[:3]):
    state_div = dl.select_one("div.anseong-search-list-book-state")
    if not state_div:
        continue
    
    print(f"\n=== DL [{i}] state_div ===")
    print("State text:", state_div.get_text(separator="|", strip=True))
    
    # table 또는 dl 또는 span 등 하위 구조
    for sub in state_div.find_all(True):
        tag = sub.name
        cls = sub.get("class", [])
        txt = sub.get_text(strip=True)[:60]
        if tag in ["table", "tr", "td", "th", "ul", "li", "span", "p"]:
            print(f"  <{tag}> class={cls}: '{txt}'")
