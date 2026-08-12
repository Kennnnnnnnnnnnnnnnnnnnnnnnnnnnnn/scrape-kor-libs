"""
가평군도서관 결과 HTML 내 정확한 소장 지점명 및 청구기호 파싱 검증
"""
from bs4 import BeautifulSoup
import re

with open("gapyeong_real_library_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

book_items = soup.select("dl.bookDataWrap")
print(f"Book items count: {len(book_items)}")

for i, item in enumerate(book_items[:5]):
    title_tag = item.select_one("dt.tit a")
    title = title_tag.text.strip() if title_tag else "None"
    title = re.sub(r"^\d+\.\s*", "", title)
    print(f"\n[{i}] Title: {title}")
    
    for dd in item.select("dd"):
        cls = dd.get("class", [])
        txt = dd.text.strip().replace("\n", " ").replace("\t", " ")
        txt = re.sub(r"\s+", " ", txt)
        print(f"  dd(class={cls}): '{txt}'")
