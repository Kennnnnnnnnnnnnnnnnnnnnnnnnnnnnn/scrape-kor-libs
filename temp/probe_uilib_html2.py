"""
의정부시 도서관 http 프로토콜 우회 검색 결과 HTML 저장 및 상세 레이아웃 구조 진단
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

# http 프로토콜 사용!
url = "http://www.uilib.net/intro/menu/10008/program/30001/plusSearchResultList.do"
params = {"searchKeyword": "파이썬", "searchKey": "ALL"}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("uilib_search.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved uilib_search.html")
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 도서 카드 탐색
    # Jnet Type A: .book Area 또는 Jnet Type B: .book_dataOuter 등
    books = soup.select(".bookArea, .book_dataOuter, .book_list, .list_content")
    print(f"Book card elements found: {len(books)}")
    if books:
        print("First book card HTML:")
        print(books[0].prettify()[:1000])
    else:
        # 혹시 div 중 클래스명에 book 이나 list 가 들어간 것 탐색
        items = soup.select("div[class*='book'], div[class*='list']")
        print(f"Div matches (book/list): {len(items)}")
        for i, item in enumerate(items[:3]):
            print(f"  [{i}] tag={item.name} class={item.get('class')}")
except Exception as e:
    print("Error:", e)
