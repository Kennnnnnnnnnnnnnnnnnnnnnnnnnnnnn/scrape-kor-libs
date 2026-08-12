"""
동작구 EUC-KR / UTF-8 인코딩 raw 바이트 파라미터 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111'
}

session.get("https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111", headers=HEADERS, verify=False)

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"

# EUC-KR 쿼리 스트링 구성
kwd_euckr = urllib.parse.quote("파이썬".encode("euc-kr"))
body_euckr = f"menu_idx=111&search_type=TITLE&search_text={kwd_euckr}&libraryCodes=ALL&booktype=BOOK&viewPage=1&rowCount=10"

r_euckr = session.post(url, data=body_euckr, headers=HEADERS, timeout=12, verify=False)
soup_euckr = BeautifulSoup(r_euckr.text, "html.parser")
cnt_euckr = soup_euckr.select_one("div.search-info")
print("EUC-KR raw body POST ->", cnt_euckr.text.strip() if cnt_euckr else "None")

# UTF-8 쿼리 스트링 구성
kwd_utf8 = urllib.parse.quote("파이썬".encode("utf-8"))
body_utf8 = f"menu_idx=111&search_type=TITLE&search_text={kwd_utf8}&libraryCodes=ALL&booktype=BOOK&viewPage=1&rowCount=10"

r_utf8 = session.post(url, data=body_utf8, headers=HEADERS, timeout=12, verify=False)
soup_utf8 = BeautifulSoup(r_utf8.text, "html.parser")
cnt_utf8 = soup_utf8.select_one("div.search-info")
print("UTF-8 raw body POST ->", cnt_utf8.text.strip() if cnt_utf8 else "None")
