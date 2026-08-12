"""
군포시도서관 raw body 및 iframe 분석
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = session.get("https://www.gunpolib.go.kr/", headers=HEADERS, timeout=8, verify=False)

print("Body length:", len(r.text))
soup = BeautifulSoup(r.text, "html.parser")

print("Iframes:", len(soup.select("iframe")))
for ifr in soup.select("iframe"):
    print("  iframe src:", ifr.get("src"))

print("Frames:", len(soup.select("frame")))
for fr in soup.select("frame"):
    print("  frame src:", fr.get("src"))

# head 또는 body에 있는 모든 external script src
for sc in soup.select("script[src]"):
    print("  Script src:", sc.get("src"))
