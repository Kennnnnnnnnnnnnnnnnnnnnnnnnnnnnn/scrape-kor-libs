"""
안성시도서관 1차 결과 HTML 내 소장 상태 및 청구기호 엘리먼트 분석
"""
from bs4 import BeautifulSoup
import re

with open("anseong_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 책 정보 카드가 보통 dd.dataType 이나 dd 혹은 dl 하위에 들어있음
book_cards = soup.select(".anseong-search-list-book-status, .book-status, div[class*='status'], .status")
print(f"Status containers found: {len(book_cards)}")

for idx, card in enumerate(book_cards[:5]):
    print(f"\n[{idx}] class={card.get('class')}:")
    print(card.prettify()[:800])
