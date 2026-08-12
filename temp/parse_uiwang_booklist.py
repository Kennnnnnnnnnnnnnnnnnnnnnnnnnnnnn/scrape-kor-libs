"""
의왕시도서관 bookList div 하위 구조 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("uiwang_result_program.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

book_list = soup.select_one("div.bookList")
if book_list:
    # 하위 구조 분석
    children = book_list.find_all(recursive=False)
    print(f"div.bookList children: {len(children)}")
    for i, ch in enumerate(children[:20]):
        cls = ch.get("class", [])
        tag = ch.name
        txt = ch.text.strip()[:80] if ch.text else ""
        print(f"  [{i}] <{tag}> class={cls} text='{txt}'")
    
    # ul > li 구조
    lis = book_list.select("ul > li")
    print(f"\nul > li items: {len(lis)}")
    for i, li in enumerate(lis[:10]):
        print(f"  [{i}] class={li.get('class', [])} text='{li.text.strip()[:100]}'")
    
    # div 구조
    divs = book_list.select("div")
    print(f"\nInner divs: {len(divs)}")
    for i, d in enumerate(divs[:20]):
        cls = d.get("class", [])
        txt = d.text.strip()[:60]
        print(f"  [{i}] class={cls} text='{txt}'")

    # a태그들
    links = book_list.select("a")
    print(f"\nInner links: {len(links)}")
    for i, a in enumerate(links[:10]):
        print(f"  [{i}] text='{a.text.strip()[:50]}' href='{a.get('href', '')[:80]}' onclick='{a.get('onclick', '')[:80]}'")
