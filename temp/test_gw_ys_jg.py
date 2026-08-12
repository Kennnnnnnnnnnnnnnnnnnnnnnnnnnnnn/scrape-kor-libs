"""
관악구, 용산구, 중구립도서관 스크래퍼 검증
"""
from scrapers.seoul import GwanakScraper, YongsanScraper, JungguScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. 관악구립도서관 (GwanakScraper) ===")
gw = GwanakScraper()
cnt, books = gw.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")

print("\n=== 2. 용산구립도서관 (YongsanScraper) ===")
ys = YongsanScraper()
cnt, books = ys.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")

print("\n=== 3. 중구립도서관 (JungguScraper) ===")
jg = JungguScraper()
cnt, books = jg.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")
