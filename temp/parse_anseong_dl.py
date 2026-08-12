"""
안성시 dl 태그 내부 상세 파싱 분석
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
print(f"Total DL items: {len(dls)}")

for i, dl in enumerate(dls[:3]):
    print(f"\n=== DL [{i}] ===")
    for tag in dl.find_all(recursive=False):
        cls = tag.get("class", [])
        txt = tag.get_text(separator='|', strip=True)[:150]
        print(f"  <{tag.name}> class={cls}: '{txt}'")
        for sub in tag.find_all(recursive=False):
            stxt = sub.get_text(separator='|', strip=True)[:100]
            print(f"    <{sub.name}> class={sub.get('class', [])}: '{stxt}'")
