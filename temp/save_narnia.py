import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from scrapers.hwaseong import HwaseongScraper

scraper = HwaseongScraper()
total, books = scraper.search("the chronicles of Narnia")

with open("narnia_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Total: {total}, Books: {len(books)}\n\n")
    from collections import defaultdict
    lib_map = defaultdict(list)
    for b in books:
        lib_map[b.library].append(b)
    
    for lib, blist in lib_map.items():
        f.write(f"도서관: [{lib}] ({len(blist)}건)\n")
        for b in blist:
            f.write(f"  - 제목: {b.title} | 청구기호: {b.call_number} | 위치: {b.location}\n")
        f.write("\n")

print("Saved to narnia_result.txt")
