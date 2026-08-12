"""
동작구립도서관 다양한 키워드 검색 실험
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.dongjak.go.kr/dj/index.do'
}

session.get("https://lib.dongjak.go.kr/dj/index.do", headers=HEADERS, verify=False)

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"
keywords = ["한국", "소설", "자바", "컴퓨터", "수학"]

for kw in keywords:
    payload = {
        "menu_idx": "111",
        "booktype": "BOOK",
        "search_type": "ALL",
        "search_text": kw
    }
    r = session.post(url, data=payload, headers=HEADERS, timeout=8, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    cnt_info = soup.select_one("div.search-info")
    print(f"Keyword '{kw}' -> {cnt_info.text.strip() if cnt_info else 'None'}")
