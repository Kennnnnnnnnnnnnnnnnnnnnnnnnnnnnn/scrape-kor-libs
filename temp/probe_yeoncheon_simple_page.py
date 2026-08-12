"""
연천군도서관 searchSimple.do 서비스 페이지 상세 분석
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

url = "https://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yeoncheon_simple_page.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yeoncheon_simple_page.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # iframe, form, script 분석
    iframes = soup.select("iframe")
    print(f"Iframes: {len(iframes)}")
    for i, ifr in enumerate(iframes):
        print(f"  Iframe[{i}] src='{ifr.get('src')}'")
        
    forms = soup.select("form")
    print(f"Forms: {len(forms)}")
    for j, form in enumerate(forms):
        print(f"  Form[{j}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
        for inp in form.select("input, select"):
            print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')}")
            
except Exception as e:
    print("Error:", e)
