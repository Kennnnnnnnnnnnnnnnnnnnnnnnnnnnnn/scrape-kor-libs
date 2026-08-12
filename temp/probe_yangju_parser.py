"""
양주시도서관 결과 HTML 내 소장 지점명 및 청구기호 추출 구조 파싱 검증
"""
from bs4 import BeautifulSoup
import re

with open("yangju_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

book_items = soup.select("dl.bookDataWrap")
print(f"Book items: {len(book_items)}")

for i, item in enumerate(book_items[:5]):
    print(f"\n--- Book [{i}] ---")
    title_tag = item.select_one("dt.tit a")
    title = title_tag.text.strip() if title_tag else "None"
    title = re.sub(r"^\d+\.\s*", "", title)
    
    author_tag = item.select_one("dd.author span")
    author = author_tag.text.strip() if author_tag else "None"
    author = re.sub(r"^(저\s*:\s*|저자\s*:\s*)", "", author)
    
    print(f"  Title: {title} | Author: {author}")
    
    # dd.site 와 dd.data 파싱
    site_spans = item.select("dd.site span")
    print(f"  Site spans count: {len(site_spans)}")
    for j, span in enumerate(site_spans):
        print(f"    Site[{j}]: '{span.text.strip()}'")
        
    data_spans = item.select("dd.data span")
    print(f"  Data spans count: {len(data_spans)}")
    for k, span in enumerate(data_spans):
        print(f"    Data[{k}]: '{span.text.strip()}'")
