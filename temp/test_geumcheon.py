"""
금천구립도서관 (GeumcheonScraper) 연동 검증
"""
from scrapers.seoul import GeumcheonScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 금천구립도서관 (GeumcheonScraper) ===")
gc = GeumcheonScraper()
cnt, books = gc.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:5]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")
