"""
유성구립도서관 결과 본문 3차 정밀 분석
"""
from bs4 import BeautifulSoup

with open("yuseong_brief_5.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
total_tag = soup.select_one("#totalCnt")
if total_tag:
    print(f"Total count text: {total_tag.text.strip()}")
else:
    print("totalCnt tag not found")

# 도서 목록
# class="bookList" 내의 구조 분석
book_list = soup.select_one(".bookList")
if book_list:
    # 각 도서 item
    # top 영역을 제외한 div.list01, list02 등 혹은 ul/li
    items = book_list.select("div.top ~ div")
    print(f"Book items found: {len(items)}")
    if items:
        print("\n=== FIRST ITEM HTML ===")
        print(items[0].prettify()[:1500])
else:
    print("bookList not found")
