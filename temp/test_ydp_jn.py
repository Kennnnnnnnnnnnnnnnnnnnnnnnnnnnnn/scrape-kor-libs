"""
영등포구립도서관 및 중랑구립도서관 연동 단독 검증
"""
from scrapers.seoul import YeongdeungpoScraper, JungnangScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. 영등포구립도서관 (YeongdeungpoScraper) ===")
ydp = YeongdeungpoScraper()
cnt1, books1 = ydp.search("파이썬")
print(f"검색 결과 총 건수: {cnt1}")
for i, b in enumerate(books1[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")

print("\n=== 2. 중랑구립도서관 (JungnangScraper) ===")
jn = JungnangScraper()
cnt2, books2 = jn.search("파이썬")
print(f"검색 결과 총 건수: {cnt2}")
for i, b in enumerate(books2[:3]):
    print(f"  [{i+1}] {b.title} | 도서관: {b.library} | 청구기호: {b.call_number}")
