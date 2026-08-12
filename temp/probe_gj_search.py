"""
광진구립도서관 (gjinfo) 실시간 수집 검증기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.gwangjinlib.seoul.kr/intro.do'
}

session.get("https://www.gwangjinlib.seoul.kr/intro.do", headers=HEADERS, verify=False)

urls = [
    "https://www.gwangjinlib.seoul.kr/gjinfo/menu/10003/program/30001/searchResultList.do",
    "https://www.gwangjinlib.seoul.kr/gjinfo/search/searchResultList.do",
    "https://www.gwangjinlib.seoul.kr/gjinfo/menu/10003/program/30001/plusSearchResultList.do"
]

payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

for url in urls:
    r = session.get(url, params=payload, headers=HEADERS, timeout=10, verify=False)
    print(f"URL: {url.split('gjinfo/')[-1]} -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
    if r.text.count("파이썬") > 1:
        soup = BeautifulSoup(r.text, "html.parser")
        with open("gwangjin_search_ok.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("★ GWANGJIN MATCH SUCCESS! ★ Saved gwangjin_search_ok.html!")
        for sel in ["dl.bookDataWrap", "div.book_dataInner", "div.bookDataWrap", "li.resultListItem"]:
            items = soup.select(sel)
            if items:
                print(f"  Selector '{sel}': {len(items)} items")
                for i, it in enumerate(items[:2]):
                    print(f"    [{i+1}] {it.text.strip()[:100]}")
