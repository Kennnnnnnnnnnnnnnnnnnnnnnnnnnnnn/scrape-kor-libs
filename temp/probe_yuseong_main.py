"""
유성구립도서관 메인페이지 검색 폼 분석
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

session = requests.Session()
session.mount('https://', SslAdapter())

url = "https://lib.yuseong.go.kr"
try:
    r = session.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"Status: {r.status_code}")
    forms = soup.select("form")
    print(f"Forms count: {len(forms)}")
    for i, f in enumerate(forms):
        print(f"Form[{i}] action={f.get('action')} method={f.get('method')}")
        for inp in f.select("input, select"):
            print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
except Exception as e:
    print(f"Error: {e}")
