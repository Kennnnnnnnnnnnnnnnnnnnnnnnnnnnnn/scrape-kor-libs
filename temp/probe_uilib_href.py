"""
의정부시 도서관(uilib.go.kr) 메인 HTML 저장 및 전체 a 태그 href 분석
"""
from bs4 import BeautifulSoup

# uilib_gnb.py 에서 가져왔던 HTML 저장 로직 재실행
import requests
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
HEADERS = {'User-Agent': 'Mozilla/5.0'}

try:
    r = session.get("https://www.uilib.go.kr/", headers=HEADERS, timeout=8, verify=False)
    with open("uilib_main.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved uilib_main.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    print("Total a tags:", len(soup.select("a")))
    
    # href 출력 (상위 40개)
    for idx, a in enumerate(soup.select("a")[:40]):
        print(f"  [{idx}] href='{a.get('href')}' txt='{a.text.strip()[:30]}'")
except Exception as e:
    print(e)
