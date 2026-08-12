"""
안산시도서관 HTML 저장 및 시흥시도서관 main.js 분석
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

# 1. 안산시도서관 HTML 저장
try:
    r = session.get("http://lib.iansan.net", headers=HEADERS, timeout=8, verify=False)
    with open("ansan_main.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved ansan_main.html")
except Exception as e:
    print("Ansan Error:", e)

# 2. 시흥시도서관 main.js 다운로드
try:
    r = session.get("https://lib.siheung.go.kr/main.js", headers=HEADERS, timeout=8, verify=False)
    with open("siheung_main.js", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved siheung_main.js. Length:", len(r.text))
except Exception as e:
    print("Siheung Error:", e)
