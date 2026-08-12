"""
의정부시도서관 검색 결과 HTML 저장 및 상세 레이아웃 구조 진단
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tls12Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
        ctx.set_ciphers('DEFAULT@SECLEVEL=0')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', Tls12Adapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

url = "https://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do"
params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
    
    with open("uilib_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved uilib_search.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Jnet 계열 도서 카드(클래스명) 탐색
    print("\n=== 도서 정보 영역 진단 ===")
    books = soup.select(".bookArea")
    print(f"Book card elements: {len(books)}")
    if books:
        # 첫 번째 카드 레이아웃 덤프
        print("First book card HTML:")
        print(books[0].prettify()[:1500])
except Exception as e:
    print("Error:", e)
