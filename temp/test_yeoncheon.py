"""
연천군도서관 YeoncheonScraper 연동 검증
"""
from scrapers.gyeonggi import YeoncheonScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

scraper = YeoncheonScraper()
cnt, books = scraper.search("파이썬")

print(f"검색 결과 건수: {cnt}")
for i, b in enumerate(books[:5]):
    print(f"[{i+1}] {b.title} | 저자: {b.author} | 도서관: {b.library} | 위치: {b.location} | 청구기호: {b.call_number}")
