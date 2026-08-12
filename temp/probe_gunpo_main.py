"""
군포시도서관 main.js 다운로드 및 API 분석
"""
import requests
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = session.get("https://www.gunpolib.go.kr/main.js?v=2026.7.22.9", headers=HEADERS, timeout=12, verify=False)
print("main.js Status:", r.status_code, "Length:", len(r.text))

with open("gunpo_main.js", "w", encoding="utf-8") as f:
    f.write(r.text)

# API URL 및 Pyxis 관련 키워드 탐색
urls = re.findall(r'https?://[^\s\'"]+', r.text)
print(f"Found URLs in main.js: {len(urls)}")
for u in urls[:20]:
    print("  URL:", u)

# API 엔드포인트 패턴 탐색
api_matches = re.findall(r'["\'](/pyxis-api/[^\s\'"]+)["\']', r.text)
print(f"\nPyxis API endpoints: {len(api_matches)}")
for m in set(api_matches[:20]):
    print("  API:", m)
