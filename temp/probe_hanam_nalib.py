"""
하남시 나룰도서관(nalib/index.do) GNB 및 검색 폼 정밀 식별
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
HEADERS = {'User-Agent': 'Mozilla/5.0'}

url = "https://www.hanamlib.go.kr/nalib/index.do"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    
    with open("hanam_nalib_main.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved hanam_nalib_main.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 폼 분석
    forms = soup.select("form")
    print(f"Forms: {len(forms)}")
    for i, form in enumerate(forms):
        print(f"  Form[{i}] action={form.get('action')} method={form.get('method')} id={form.get('id')}")
        for inp in form.select("input, select"):
            print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
            
    # 검색 a 링크
    a_search = [a for a in soup.select("a") if a.get("href") and any(w in a.get("href").lower() for w in ["search", "result", "list"])]
    print(f"\n=== 하남 도서검색 관련 링크 ({len(a_search)}개) ===")
    for j, a in enumerate(a_search[:20]):
        print(f"  [{j}] txt='{a.text.strip()}' -> href='{a.get('href')}'")
        
except Exception as e:
    print("Error:", e)
