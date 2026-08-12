"""
Type A (구리시, 과천시) 및 Type B (성남시) HTML 구조 정밀 분석
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def analyze_a(city, domain):
    url = f"https://{domain}/intro/menu/10003/program/30001/searchResultList.do"
    try:
        r = requests.get(url, params={"searchType": "SIMPLE", "searchKeyword": "파이썬"}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("#bookList > div > ul > li")
        if not items:
            items = soup.select("#bookList li")
        print(f"\n[{city}] items found: {len(items)}")
        if items:
            print(f"--- FIRST ITEM HTML ---")
            print(str(items[0])[:2000])
    except Exception as e:
        print(f"[{city}] Error: {e}")

def analyze_b_seongnam():
    url = "https://www.snlib.go.kr/intro/menu/10181/program/30012/plusSearchResultList.do"
    try:
        r = requests.get(url, params={"searchType": "SIMPLE", "searchCategory": "BOOK", "searchKey": "TITLE", "searchKeyword": "파이썬"}, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("ul.resultList > li")
        print(f"\n[성남시] items found: {len(items)}")
        if items:
            print(f"--- FIRST ITEM HTML ---")
            print(str(items[0])[:2000])
    except Exception as e:
        print(f"[성남시] Error: {e}")

print("=== Type A (구리, 과천) 분석 ===")
analyze_a("구리시", "www.gurilib.go.kr")
analyze_a("과천시", "www.gclib.go.kr")

print("\n=== Type B (성남시) 분석 ===")
analyze_b_seongnam()
