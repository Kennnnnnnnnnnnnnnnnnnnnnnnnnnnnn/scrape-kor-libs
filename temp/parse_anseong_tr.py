"""
안성시 state_div 내 tbody tr 및 onclick 분석
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
    print(f"\n=== DL [{i}] ===")
    tbodys = dl.select("table tbody tr")
    print("tbody tr count:", len(tbodys))
    for j, tr in enumerate(tbodys):
        tds = [td.get_text(strip=True) for td in tr.select("td")]
        print(f"  tr[{j}]: {tds}")
    
    # 버튼/링크의 onclick
    for btn in dl.select("button, a"):
        onc = btn.get("onclick", "")
        if onc:
            print(f"  btn/a onclick: '{btn.text.strip()}' -> {onc}")
