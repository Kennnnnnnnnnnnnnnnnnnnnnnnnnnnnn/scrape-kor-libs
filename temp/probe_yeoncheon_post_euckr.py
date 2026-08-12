"""
연천군도서관 EUC-KR 바디 POST 수동 인코딩 최종 실시간 검증
"""
import requests
import urllib.parse
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
session.mount('http://', SslAdapter())
session.mount('https://', SslAdapter())

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'http://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# 1. 1차 접속 (세션 획득)
session.get("http://library.yeoncheon.go.kr/menu/10039/program/30005/searchSimple.do", headers=HEADERS, timeout=8)

url = "http://library.yeoncheon.go.kr/menu/10039/program/30005/searchResultList.do"

# 2. 바디 데이터를 euc-kr 로 수동 바이트코딩 직렬화!
kwd_euckr = "파이썬".encode("euc-kr")
payload_dict = [
    ("searchLibraryArr", "MA"),
    ("searchLibraryArr", "BR"),
    ("searchLibraryArr", "ME"),
    ("searchLibraryArr", "MD"),
    ("searchLibraryArr", "MF"),
    ("searchLibraryArr", "MG"),
    ("searchLibrary", "ALL"),
    ("searchKeyword", kwd_euckr),  # 바이트 스트림 대입!
    ("searchType", "SIMPLE"),
    ("searchKey", "ALL")
]

# urlencode 수행 시 euc-kr 인코딩 강제 매핑!
body_enc = urllib.parse.urlencode(payload_dict, encoding="euc-kr")
print(f"EUC-KR Encoded Body: {body_enc[:120]}...")

try:
    # 수동 인코딩된 바이트 문자열을 data 인자로 직접 전달!
    r = session.post(url, data=body_enc.encode("ascii"), headers=HEADERS, timeout=12)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("yeoncheon_real_post_euckr.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved yeoncheon_real_post_euckr.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    book_items = soup.select("dl.bookDataWrap")
    print(f"Book items: {len(book_items)}")
    
    for i, item in enumerate(book_items[:3]):
        title = item.select_one("dt.tit a").text.strip()
        print(f"  [{i}] Title: {title}")
        
except Exception as e:
    print("Error:", e)
