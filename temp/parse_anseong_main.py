"""
안성시도서관 (anseong.go.kr/library/main.do) 검색 폼 및 링크 상세 분석
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

r = session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

# 모든 폼 출력
forms = soup.select("form")
print(f"Forms count: {len(forms)}")
for i, form in enumerate(forms):
    print(f"\nForm[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}' name='{form.get('name')}'")
    for inp in form.select("input"):
        print(f"  input: name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")

# search/자료검색 관련 a 태그
print("\nSearch Links:")
for a in soup.select("a[href*='search'], a[href*='Search'], a[onclick*='search'], a[onclick*='Search']"):
    print(f"  text='{a.text.strip()[:30]}' href='{a.get('href', '')}' onclick='{a.get('onclick', '')}'")
