"""
광주시도서관 q 파라미터 검색 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import sys

sys.stdout.reconfigure(encoding='utf-8')
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.gjcity.go.kr/'
}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"

# 1. GET 방식 q=파이썬
print("=== GET q=파이썬 ===")
r_get = session.get(url, params={"q": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL"}, headers=HEADERS, timeout=10, verify=False)
print("GET Status:", r_get.status_code, "Len:", len(r_get.text), "파이썬 count:", r_get.text.count("파이썬"))

# 2. POST 방식 q=파이썬
print("\n=== POST q=파이썬 ===")
r_post = session.post(url, data={"q": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL"}, headers=HEADERS, timeout=10, verify=False)
print("POST Status:", r_post.status_code, "Len:", len(r_post.text), "파이썬 count:", r_post.text.count("파이썬"))

if r_get.text.count("파이썬") > 1 or r_post.text.count("파이썬") > 1:
    print("  ★ GWANGJU SEARCH SUCCESS ★")
    res_text = r_get.text if r_get.text.count("파이썬") > 1 else r_post.text
    with open("gwangju_q_success.html", "w", encoding="utf-8") as f:
        f.write(res_text)
    
    soup = BeautifulSoup(res_text, "html.parser")
    # 항목 리스트 추출
    for sel in ["dl.bookDataWrap", "div.resultItem", "li.resultListItem", "tr.resultListItem", "table tbody tr"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
