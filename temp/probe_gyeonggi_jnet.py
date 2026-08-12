"""
의정부시, 군포시 도서관 JNET 계열 및 통합검색 후보 URL 다각도 진단
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

CANDIDATES = [
    # 의정부시 후보들
    ("의정부시", "https://www.uilib.go.kr/search/searchResultList.do"),
    ("의정부시", "https://www.uilib.go.kr/intro/searchResultList.do"),
    ("의정부시", "https://www.uilib.go.kr/intro/program/plusSearchResultList.do"),
    ("의정부시", "https://www.uilib.go.kr/intro/menu/10008/program/30001/plusSearchResultList.do"), # 강남/동작/송파 등 Type B
    ("의정부시", "https://www.uilib.go.kr/intro/menu/10009/program/30001/plusSearchResultList.do"),
    ("의정부시", "https://www.uilib.go.kr/intro/menu/10041/program/30001/plusSearchResultList.do"),
    
    # 군포시 후보들
    ("군포시", "https://www.gunpolib.go.kr/search/searchResultList.do"),
    ("군포시", "https://www.gunpolib.go.kr/intro/searchResultList.do"),
    ("군포시", "https://www.gunpolib.go.kr/intro/program/plusSearchResultList.do"),
    ("군포시", "https://www.gunpolib.go.kr/intro/menu/10008/program/30001/plusSearchResultList.do"),
    ("군포시", "https://www.gunpolib.go.kr/intro/menu/10041/program/30001/plusSearchResultList.do")
]

params_set = [
    # 일반 Jnet Type A
    {"searchKeyword": "파이썬", "searchKey": "ALL"},
    # 일반 Jnet Type B
    {"searchKeyword": "파이썬", "searchKey": "ALL", "searchManageCode": "ALL", "topSearchCondition": "ALL"}
]

for name, url in CANDIDATES:
    print(f"\n--- {name} -> {url} ---")
    for idx, params in enumerate(params_set):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=6, verify=False)
            print(f"  Params[{idx}] -> Status: {r.status_code}, Length: {len(r.text)}")
            if r.status_code == 200 and len(r.text) > 4000:
                soup = BeautifulSoup(r.text, "html.parser")
                # 결과 수 카운트 태그가 있는지 확인
                total_tag = soup.select_one("#totalCnt, .totalCnt, .search_total, .search_count")
                total_txt = total_tag.text.strip() if total_tag else "No totalCnt"
                print(f"    [SUCCESS!!!] Total count tag: {total_txt}")
                
                # 도서 제목 태그
                titles = soup.select("a.book_name, .bookArea a.book_name, .title a, a[href*='plusSearchDetail']")
                print(f"    Titles found: {len(titles)}")
                for i, t in enumerate(titles[:3]):
                    print(f"      [{i}] Title: {t.text.strip()}")
        except Exception as e:
            print(f"  Params[{idx}] -> Error: {e}")
