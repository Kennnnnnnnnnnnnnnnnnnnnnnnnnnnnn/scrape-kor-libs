"""
인천광역시교육청도서관 (IncheonEducationScraper) 연동 단독 검증
"""
from scrapers.incheon import IncheonEducationScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 인천광역시교육청도서관 (IncheonEducationScraper) ===")
ice = IncheonEducationScraper()
cnt, books = ice.search("파이썬")
print(f"검색 결과 총 건수: {cnt}")
for i, b in enumerate(books[:5]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 청구기호: {b.call_number}")
