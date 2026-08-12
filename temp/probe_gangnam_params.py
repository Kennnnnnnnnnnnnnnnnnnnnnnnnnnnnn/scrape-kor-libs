"""
강남구립도서관 검색 파라미터 추가 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://library.gangnam.go.kr/intro/plusSearchResultList.do"

# 테스트 케이스
test_cases = [
    # 1. searchKey="ALL" 추가한 영어 검색
    {"searchKeyword": "python", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL"},
    # 2. searchKey="ALL" 추가한 한글 검색
    {"searchKeyword": "파이썬", "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL"},
    # 3. EUC-KR 수동 인코딩 한글 검색
    {"searchKeyword": "파이썬".encode("euc-kr"), "searchType": "SIMPLE", "searchCategory": "ALL", "searchKey": "ALL", "searchLibrary": "ALL"}
]

for i, p in enumerate(test_cases):
    try:
        r = requests.get(url, params=p, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 전체(N) 건수가 나오는지 확인
        cnt_matches = []
        for a in soup.select("a"):
            txt = a.text.strip()
            if "전체(" in txt or "단행본(" in txt:
                cnt_matches.append(txt)
                
        print(f"Case {i} -> Status: {r.status_code}, Length: {len(r.text)}, Counts: {cnt_matches}")
        
        # 책 제목 링크들이 발견되는지 확인
        titles = soup.select("ul.resultList dt.tit a")
        if titles:
            print(f"  [SUCCESS] Found {len(titles)} titles. First: {titles[0].text.strip()}")
    except Exception as e:
        print(f"Case {i} -> Error: {e}")
