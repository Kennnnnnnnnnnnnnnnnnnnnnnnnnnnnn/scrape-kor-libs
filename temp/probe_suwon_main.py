"""
수원시 도서관 메인페이지 HTML UTF-8 파일 저장 및 검색 폼 분석
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

try:
    r = s.get('https://www.suwonlib.go.kr', headers={'User-Agent':'Mozilla/5.0'}, verify=False, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    print("Status:", r.status_code)
    
    # 모든 form과 스크립트 출력
    forms = soup.select("form")
    print("Forms found:", len(forms))
    for i, f in enumerate(forms):
        print(f"Form[{i}] action={f.get('action')} method={f.get('method')}")
        for inp in f.select("input, select"):
            print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
            
    # 스크립트의 검색 패턴 출력
    print("\n=== Scripts search match ===")
    for i, sc in enumerate(soup.select("script")):
        txt = sc.text
        if any(w in txt for w in ["search", "Search", "submit", "action"]):
            print(f"Script[{i}]:")
            for line in txt.split("\n"):
                if any(w in line for w in ["action", "submit", "href", "search"]):
                    print(f"  {line.strip()[:100]}")
except Exception as e:
    print("Error:", e)
