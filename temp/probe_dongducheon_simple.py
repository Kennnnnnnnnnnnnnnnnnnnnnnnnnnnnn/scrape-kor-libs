"""
동두천시도서관 iframe 검색 메인 페이지(/plusSearchSimple.do) 내 지점코드 전수 식별
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

url = "https://lib.ddc.go.kr/kolaseek/plus/search/plusSearchSimple.do?searchLibrary=ALL"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("dongducheon_simple.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved dongducheon_simple.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # checkbox, option 등 탐색
    inputs = soup.select("input[name*='LibraryArr'], input[type='checkbox']")
    print(f"Inputs count: {len(inputs)}")
    for inp in inputs:
        print(f"  Input: name='{inp.get('name')}' value='{inp.get('value')}' id='{inp.get('id')}'")
        
    options = soup.select("option")
    print(f"Options count: {len(options)}")
    for opt in options:
        print(f"  Option: value='{opt.get('value')}' text='{opt.text.strip()}'")
except Exception as e:
    print("Error:", e)
