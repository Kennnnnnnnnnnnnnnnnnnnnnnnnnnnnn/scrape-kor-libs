"""
안양시립도서관 스크립트 태그 덤프
"""
from bs4 import BeautifulSoup

with open("anyang_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script[src]")
print(f"Scripts: {len(scripts)}")
for sc in scripts:
    print("  Src:", sc.get("src"))
