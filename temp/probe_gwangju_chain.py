"""
GwangjuScraper GET/POST 세션 릴레이 방어 우회 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import re
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do'
}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"

# 1. 메인 접속으로 쿠키 생성
r1 = session.get("https://lib.gjcity.go.kr/intro/index.do", headers=headers, timeout=10, verify=False)
print("1. Intro status:", r1.status_code)

# 2. 검색 폼 페이지 GET 접속으로 JSESSIONID 및 세션 컨텍스트 형성
r2 = session.get(url, headers=headers, timeout=10, verify=False)
print("2. Form page GET status:", r2.status_code)

# 3. 폼 데이터를 그대로 제출하되 GET 방식으로 파라미터 전달 시도
params = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}
r3 = session.get(url, params=params, headers=headers, timeout=10, verify=False)
print("3. Search GET status:", r3.status_code, "Len:", len(r3.text), "파이썬 count:", r3.text.count("파이썬"))

# 4. POST 방식 세션 제출 시도
r4 = session.post(url, data=params, headers=headers, timeout=10, verify=False)
print("4. Search POST status:", r4.status_code, "Len:", len(r4.text), "파이썬 count:", r4.text.count("파이썬"))

if r3.text.count("파이썬") > 0 or r4.text.count("파이썬") > 0:
    res_text = r3.text if r3.text.count("파이썬") > 0 else r4.text
    soup = BeautifulSoup(res_text, "html.parser")
    items = soup.select("dl.bookDataWrap")
    print(f"  ★ GWANGJU SUCCESS! items count: {len(items)} ★")
    for i, item in enumerate(items[:3]):
        title_tag = item.select_one("dt.tit a")
        print(f"    [{i+1}] {title_tag.text.strip() if title_tag else 'None'}")
