"""
성동구립도서관 (SeongdongScraper) 연동 단독 검증
"""
from scrapers.seoul import SeongdongScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 성동구립도서관 (SeongdongScraper) ===")
sd = SeongdongScraper()
cnt, books = sd.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:5]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 위치: {b.location}")
