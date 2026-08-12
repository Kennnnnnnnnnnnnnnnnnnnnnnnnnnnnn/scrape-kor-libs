"""
강남구립도서관 plusSearchResultList.do 검색 요청 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://library.gangnam.go.kr/intro/plusSearchResultList.do"
params = {
    "searchKeyword": "파이썬",
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchLibrary": "ALL"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, "html.parser")
    with open("gangnam_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    # 총 건수
    print("\n=== 총 건수 텍스트 ===")
    total_tag = soup.select_one(".result_screen strong.highlight") or soup.select_one("strong.highlight")
    if total_tag:
        print("  Total Tag Text:", total_tag.text.strip())
        
    # 책 제목 목록
    print("\n=== 제목 목록 ===")
    titles = soup.select("ul.resultList > li dt.tit a")
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()}")
except Exception as e:
    print("Error:", e)
