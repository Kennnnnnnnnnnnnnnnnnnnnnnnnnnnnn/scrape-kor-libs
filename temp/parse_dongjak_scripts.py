"""
동작구립도서관 메인 인덱스 스크립트 목록 추출
"""
from bs4 import BeautifulSoup

with open("dongjak_search_with_libs.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# script[src] 태그들 전부 덤프
scripts = soup.select("script[src]")
print(f"Scripts: {len(scripts)}")
for sc in scripts:
    print("  Src:", sc.get("src"))
