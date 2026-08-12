"""
광명시도서관 index.php 실시간 검색 및 청구기호 추출 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://gmlib.gm.go.kr/front/index.php"
params = {
    "g_page": "search",
    "m_page": "search01",
    "searchWord": "파이썬"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gwangmyeong_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 총 건수 및 결과 목록
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    # 일반적인 table 이나 list 구조 탐색
    titles = soup.select("a[href*='search02'], .title a, a[href*='book_detail']")
    if not titles:
        # 광범위한 a 태그 내 텍스트 매칭
        titles = [a for a in soup.select("a") if a.get("href") and "detail" in a.get("href")]
        
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:8]):
        # t가 bs4 element 인 경우와 일반 string 인 경우 처리
        txt = t.text.strip() if hasattr(t, "text") else str(t)
        href = t.get("href") if hasattr(t, "get") else ""
        print(f"  [{i}] Title: {txt} | Href: {href}")
        
    # '파이썬' 단어 카운트
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
