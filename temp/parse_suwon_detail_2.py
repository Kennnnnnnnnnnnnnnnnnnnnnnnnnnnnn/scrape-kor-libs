"""
수원시 모바일 결과 리스트 태그 구조 상세 분석
"""
from bs4 import BeautifulSoup

with open("suwon_mobile.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

book_lists = soup.select(".sR_list.sR_list_book")
print(f"Lists found count: {len(book_lists)}")

for i, lst in enumerate(book_lists):
    items = lst.select("li, div.book_tbl, tr")
    print(f"List[{i}] items count: {len(items)}")
    if items:
        print("\n=== FIRST ITEM HTML ===")
        print(items[0].prettify()[:2500])
        break
else:
    # 전체 HTML에서 sR_list 클래스를 가진 요소를 그냥 출력
    gen_list = soup.select(".sR_list")
    print(f"Generic sR_list found: {len(gen_list)}")
    for j, lst in enumerate(gen_list):
        print(f"List[{j}] tag={lst.name} items={len(lst.select('li, tr, div'))}")
        if len(lst.text) > 200:
            print(lst.prettify()[:1500])
            break
