"""
동작구 libraryCodes 파라미터 전 세트 제출 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111'
}

session.get("https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111", headers=HEADERS, verify=False)

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"

payload_full = [
    ("menu_idx", "111"),
    ("search_type", "TITLE"),
    ("search_text", "파이썬"),
    ("libraryCodes", "ALL"),
    ("_libraryCodes", "on"),
    ("libraryCodes", "GuALL"),
    ("_libraryCodes", "on"),
    ("libraryCodes", "DongALL"),
    ("_libraryCodes", "on"),
    ("libraryCodes", "SiALL"),
    ("_libraryCodes", "on"),
    ("booktype", "BOOK"),
    ("viewPage", "1"),
    ("rowCount", "10")
]

r = session.post(url, data=payload_full, headers=HEADERS, timeout=12, verify=False)
print("Full POST Status:", r.status_code, "Len:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")
cnt_info = soup.select_one("div.search-info")
print("search-info text:", cnt_info.text.strip() if cnt_info else "None")

if "총 0건" not in r.text and "0건이" not in r.text and len(r.text) > 20000:
    print("  ★ DONGJAK FULL MATCH SUCCESS! ★")
    with open("dongjak_full_ok.html", "w", encoding="utf-8") as f:
        f.write(r.text)
