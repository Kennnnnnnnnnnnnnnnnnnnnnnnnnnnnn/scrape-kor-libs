"""
송파구립도서관 직접 searchResultList.do 검색 요청 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.splib.or.kr/intro/program/plusSearchResultList.do"
params = {
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE",
    "searchCategory": "BOOK",
    "searchKey": "ALL",
    "searchLibrary": "ALL"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    with open("songpa_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    # 전체(N) 건수 파싱 확인
    cnt_matches = []
    for a in soup.select("a"):
        txt = a.text.strip()
        if "전체(" in txt or "단행본(" in txt:
            cnt_matches.append(txt)
    print("Counts:", cnt_matches)
    
    # 책 제목 목록
    print("\n=== 제목 목록 ===")
    titles = soup.select("ul.resultList dt.tit a")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()}")
except Exception as e:
    print("Error:", e)
