"""
수원시 도서관 모바일 검색 및 slib_search.asp 검색 엔드포인트 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

s = requests.Session()
s.mount('https://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 모바일 검색 테스트
try:
    r = s.get('https://mob.suwonlib.go.kr/search', params={'searchWord': '파이썬'}, headers=HEADERS, verify=False, timeout=10)
    print(f"[Mobile Search] Status: {r.status_code}, Length: {len(r.text)}")
    with open("suwon_mobile.html", "w", encoding="utf-8") as f:
        f.write(r.text)
except Exception as e:
    print(f"[Mobile Search] Error: {e}")

# 2. ASP 검색 테스트
try:
    r = s.post('https://www.suwonlib.go.kr/intro/slib_search.asp', data={'keyfield': '파이썬'}, headers=HEADERS, verify=False, timeout=10)
    print(f"[ASP Search] Status: {r.status_code}, Length: {len(r.text)}")
    with open("suwon_asp.html", "w", encoding="utf-8") as f:
        f.write(r.text)
except Exception as e:
    print(f"[ASP Search] Error: {e}")
