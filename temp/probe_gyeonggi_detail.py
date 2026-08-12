"""
부천시 HTML 소스 덤프 및 안양시 SSL 우회 분석
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

print("=== 1. 부천시도서관 HTML 덤프 ===")
try:
    r = session.get("https://www.bcl.go.kr", headers=HEADERS, timeout=8, verify=False)
    print("Length:", len(r.text))
    print(r.text[:1500])
except Exception as e:
    print("Bucheon Error:", e)

print("\n=== 2. 안양시도서관 SSL 우회 폼 분석 ===")
try:
    r = session.get("https://lib.anyang.go.kr", headers=HEADERS, timeout=8, verify=False)
    print("Final URL:", r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 폼
    forms = soup.select("form")
    print("Forms:", len(forms))
    for i, f in enumerate(forms):
        print(f"  Form[{i}] action={f.get('action')} method={f.get('method')}")
        for inp in f.select("input, select"):
            print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
            
    # 스크립트
    for j, sc in enumerate(soup.select("script")):
        txt = sc.text
        if any(w in txt for w in ["search", "Search", "action"]):
            print(f"  Script[{j}] has search/action context:")
            for line in txt.split("\n"):
                if any(w in line for w in ["location", "href", "action", "search"]):
                    print(f"    {line.strip()[:100]}")
except Exception as e:
    print("Anyang Error:", e)
