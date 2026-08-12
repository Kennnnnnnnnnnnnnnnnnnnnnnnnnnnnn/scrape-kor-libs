"""
군포시, 파주시 도서관 인덱스 게이트웨이 및 리다이렉션 정밀 분석
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

TARGETS = {
    "군포시": "https://www.gunpolib.go.kr",
    "파주시": "https://lib.paju.go.kr"
}

for name, base_url in TARGETS.items():
    print(f"\n=== {name} ({base_url}) 분석 ===")
    try:
        r = session.get(base_url, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
        print("  Status:", r.status_code)
        print("  Location:", r.headers.get("Location"))
        print("  Cookies:", session.cookies.get_dict())
        
        # 만약 리다이렉트가 존재한다면 그곳으로 2차 진입
        loc = r.headers.get("Location")
        if loc:
            if loc.startswith("/"):
                loc = base_url + loc
            print(f"  Follow location: {loc}")
            r2 = session.get(loc, headers=HEADERS, timeout=8, verify=False, allow_redirects=False)
            print("    Status 2:", r2.status_code)
            print("    Location 2:", r2.headers.get("Location"))
            html = r2.text
        else:
            html = r.text
            
        soup = BeautifulSoup(html, "html.parser")
        
        # 스크립트 중 리다이렉트 구문 분석
        for idx, sc in enumerate(soup.select("script")):
            txt = sc.text
            if "location.href" in txt or "location.replace" in txt or "window.location" in txt:
                print(f"    Script[{idx}] redirect snippet:")
                for line in txt.split("\n"):
                    if any(w in line for w in ["location", "href", "replace"]):
                        print(f"      {line.strip()[:120]}")
                        
        # GNB 혹은 검색 관련 a 태그
        a_links = [a for a in soup.select("a") if a.get("href")]
        print(f"    Total a links: {len(a_links)}")
        for a_idx, a in enumerate(a_links[:15]):
            print(f"      [{a_idx}] href='{a.get('href')}' txt='{a.text.strip()[:30]}'")
            
    except Exception as e:
        print(f"  Error: {e}")
