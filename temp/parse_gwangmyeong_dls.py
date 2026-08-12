"""
광명시도서관 DLS 결과 상세 레이아웃 구조 분석 (f-string 문법 에러 해소)
"""
from bs4 import BeautifulSoup
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. 테이블 탐색
tables = soup.select("table")
print(f"Tables found: {len(tables)}")
for i, table in enumerate(tables):
    headers = [th.text.strip() for th in table.select("th")]
    print(f"  Table[{i}] Headers: {headers}")
    rows = table.select("tbody tr")
    print(f"    Rows count: {len(rows)}")
    if rows:
        row_txt = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in rows[0].select('td')[:5]]
        print("    First row cols:", row_txt)

# 2. 만약 테이블이 아니라면 dl / ul 리스트형태 탐색
if not tables or len(tables) < 2:
    print("\n=== 2. List / DL Layout Search ===")
    lists = soup.select(".list_content, .book_list, .search_list, ul.list > li")
    print(f"List items found: {len(lists)}")
    
    # 텍스트 단락들을 좀 더 광범위하게 확인하기 위해 a 태그 주변의 td 나 div 구조를 덤프
    items = soup.select("a[href*='searchResultDetail']")
    print(f"Detail link tag parent structures (Top 3):")
    for j, a in enumerate(items[:3]):
        p = a.find_parent("tr") or a.find_parent("li") or a.find_parent("div")
        if p:
            print(f"  Parent[{j}] ({p.name} class={p.get('class')}):")
            # 안전하게 출력
            p_html = p.prettify()[:1000]
            print(p_html)
