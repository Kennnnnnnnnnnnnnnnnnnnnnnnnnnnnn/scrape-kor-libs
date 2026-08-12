"""
부천시도서관 진짜 루트(site/main/introNew) 검색 구조 분석
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

url = "https://www.bcl.go.kr/site/main/introNew"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Final URL:", r.url)
    print("Status:", r.status_code)
    
    html_text = r.text.lstrip('\ufeff')
    with open("bucheon_intro.html", "w", encoding="utf-8") as f:
        f.write(html_text)
        
    soup = BeautifulSoup(html_text, "html.parser")
    
    # 폼 분석
    forms = soup.select("form")
    print("Forms:", len(forms))
    for i, f in enumerate(forms):
        print(f"  Form[{i}] action={f.get('action')} method={f.get('method')}")
        for inp in f.select("input, select"):
            print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
            
    # 스크립트 분석
    for j, sc in enumerate(soup.select("script")):
        txt = sc.text
        if any(w in txt for w in ["search", "Search", "action"]):
            print(f"  Script[{j}] has search/action context:")
            for line in txt.split("\n"):
                if any(w in line for w in ["location", "href", "action", "search"]):
                    print(f"    {line.strip()[:100]}")
                    
except Exception as e:
    print("Error:", e)
