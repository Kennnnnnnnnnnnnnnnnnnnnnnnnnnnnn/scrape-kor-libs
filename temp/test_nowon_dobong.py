"""
노원구립도서관 및 도봉구립도서관 연동 단독 검증
"""
from scrapers.seoul import NowonScraper, DobongScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. 노원구립도서관 (NowonScraper) ===")
nowon = NowonScraper()
cnt1, books1 = nowon.search("파이썬")
print(f"검색 결과 총 건수: {cnt1}")
for i, b in enumerate(books1[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 위치: {b.location}")

print("\n=== 2. 도봉구립도서관 (DobongScraper) ===")
dobong = DobongScraper()
cnt2, books2 = dobong.search("파이썬")
print(f"검색 결과 수집 건수: {cnt2}")
for i, b in enumerate(books2[:3]):
    print(f"  [{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 위치: {b.location}")
