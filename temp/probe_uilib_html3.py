"""
의정부시 도서관(uilib.net) 진짜 HTTPS 200 성공 연동 및 도서 파싱
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = "https://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do"
params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

try:
    r = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("uilib_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved uilib_search.html successfully!")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 1. 22487바이트 정도면 목록 검색결과 페이지가 맞는지 타이틀 확인
    print("Title:", soup.title.text.strip() if soup.title else "No Title")
    
    # 2. 책 목록 파싱 테스트
    print("\n=== 책 제목 탐색 ===")
    titles = soup.select(".bookArea a.book_name, a.book_name, .title a, a[href*='plusSearchDetail']")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()}")
        
except Exception as e:
    print("Error:", e)
