"""
의정부시 도서관 진짜 메인(main/index.do) GNB 링크 파싱 및 통합검색 경로 식별
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

url = "https://www.uilib.go.kr/main/index.do"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    
    with open("uilib_real_main.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved uilib_real_main.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.select("a")
    print("Total a tags:", len(a_tags))
    
    # 검색/자료 관련 링크 수집
    links = []
    for a in a_tags:
        href = a.get("href", "")
        txt = a.text.strip().replace("\n", " ")
        links.append((txt, href))
        
    # 'search' 나 'SearchResult' 나 'searchResultList' 가 들어있는 href 필터링
    print("\n=== 'search' 관련 href 필터링 ===")
    found = 0
    for idx, (t, h) in enumerate(links):
        if any(w in h.lower() for w in ["search", "plussearch", "result", "list"]):
            print(f"  [{idx}] txt='{t}' -> href='{h}'")
            found += 1
    print("Found:", found)
    
except Exception as e:
    print("Error:", e)
