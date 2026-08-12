"""
동작구 librarySearch POST 파라미터 실시간 검증
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111'
}

session.get("https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111", headers=headers, verify=False)

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"

payloads = [
    {
        "menu_idx": "111",
        "search_type": "ALL",
        "search_text": "파이썬",
        "libraryCodes": "ALL",
        "booktype": "BOOK",
        "viewPage": "1",
        "rowCount": "10"
    },
    {
        "menu_idx": "111",
        "search_type": "TITLE",
        "search_text": "파이썬",
        "libraryCodes": "ALL",
        "booktype": "BOOK",
        "viewPage": "1",
        "rowCount": "10"
    },
    {
        "menu_idx": "111",
        "search_type": "TITLE",
        "search_text": "파이썬",
        "libraryCodes": "GuALL",
        "booktype": "BOOK",
        "viewPage": "1",
        "rowCount": "10"
    }
]

for i, p in enumerate(payloads):
    r = session.post(url, data=p, headers=headers, timeout=12, verify=False)
    print(f"[{i}] POST Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
    
    soup = BeautifulSoup(r.text, "html.parser")
    cnt_info = soup.select_one("div.search-info")
    print("    search-info text:", cnt_info.text.strip() if cnt_info else "None")
    
    if r.text.count("파이썬") > 5:
        print(f"  ★ DONGJAK MATCH Payload[{i}] ★")
        with open(f"dongjak_match_{i}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
