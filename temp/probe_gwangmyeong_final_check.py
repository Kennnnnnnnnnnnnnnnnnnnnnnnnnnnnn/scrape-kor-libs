"""
광명시도서관 결과 데이터 깨짐 및 값 유무 최종 진단
"""
from scrapers.gyeonggi import GwangmyeongScraper

scraper = GwangmyeongScraper()
total, books = scraper.search("파이썬")

print(f"Total: {total}, Return: {len(books)}")
with open("gwangmyeong_debug_out.txt", "w", encoding="utf-8") as f:
    for idx, b in enumerate(books):
        f.write(f"Book[{idx}]:\n")
        f.write(f"  Title: {b.title}\n")
        f.write(f"  Author: {b.author}\n")
        f.write(f"  Library: {b.library}\n")
        f.write(f"  CallNumber: {b.call_number}\n")
        f.write(f"  Location: {b.location}\n")
print("Saved to gwangmyeong_debug_out.txt successfully!")
