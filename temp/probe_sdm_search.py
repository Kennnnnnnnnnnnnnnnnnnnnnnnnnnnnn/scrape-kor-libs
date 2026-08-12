"""
서대문구립도서관 JNET 도서 검색 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://lib.sdm.or.kr/sdmlib/menu/10003/program/30001/searchResultList.do",
    "https://lib.sdm.or.kr/sdmlib/menu/10003/program/30001/plusSearchResultList.do",
    "https://lib.sdm.or.kr/sdmlib/program/searchResultList.do",
]

payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

for url in urls:
    try:
        r = session.get(url, params=payload, headers=HEADERS, timeout=10, verify=False)
        count = r.text.count("파이썬")
        print(f"URL: {url.split('sdmlib/')[-1]} -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {count}")
        if count > 1:
            soup = BeautifulSoup(r.text, "html.parser")
            for sel in ["dl.bookDataWrap", "div.book_dataInner", "div.bookDataWrap", "li.resultListItem"]:
                items = soup.select(sel)
                if items:
                    print(f"  Selector '{sel}': {len(items)} items")
                    for i, it in enumerate(items[:2]):
                        print(f"    [{i+1}] {it.text.strip()[:100]}")
    except Exception as e:
        print(f"  Error: {e}")
