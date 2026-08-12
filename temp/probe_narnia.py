import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from scrapers.hwaseong import HwaseongScraper
from title_utils import strip_title

title = "the chronicles of Narnia"
search_title = strip_title(title)
print(f"Original Title: '{title}' -> Strip Title: '{search_title}'")

scraper = HwaseongScraper()
total, books = scraper.search(search_title)
print(f"Total count returned by scraper: {total}, books parsed: {len(books)}")

from collections import defaultdict
lib_map = defaultdict(list)
for b in books:
    lib_map[b.library].append(b)

print(f"\nDiscovered libraries ({len(lib_map)}):")
for lib, blist in lib_map.items():
    print(f" - {lib}: {len(blist)}건")
    for b in blist[:2]:
        print(f"      Title: {b.title} | CallNo: {b.call_number} | Loc: {b.location}")
