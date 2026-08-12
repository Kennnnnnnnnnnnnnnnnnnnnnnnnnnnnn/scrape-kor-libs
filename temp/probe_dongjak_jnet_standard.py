"""
동작구 JNET 표준 폼 응답 상세 파싱
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

payload = {
    "menu_idx": "111",
    "search_text": "파이썬",
    "search_type": "TITLE",
    "search_library": "ALL"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
print("Status:", r.status_code, "Len:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")
with open("dongjak_jnet_standard.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Text snippets:")
for el in soup.find_all(["div", "p", "span", "b", "strong"]):
    txt = el.text.strip().replace("\n", " ")
    if "검색결과" in txt or "건" in txt and "검색" in txt:
        print(" ", el.name, el.get("class"), "->", txt[:100])
