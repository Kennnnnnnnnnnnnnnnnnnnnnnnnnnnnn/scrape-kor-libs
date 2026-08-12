from scrapers.seoul import NowonScraper

scraper = NowonScraper()
total, books = scraper.search("파친코")

print(f"Total: {total}, Parsed Books: {len(books)}")

from collections import defaultdict
libs = defaultdict(list)
for b in books:
    libs[b.library].append(b)

print(f"\n[노원구립도서관 수집 결과 (총 {len(libs)}개 도서관)]:")
for lib, blist in libs.items():
    print(f"\n도서관: {lib} ({len(blist)}건)")
    for b in blist[:3]:
        print(f"  - 제목: {b.title} | 청구기호: '{b.call_number}' | 위치: {b.location}")
