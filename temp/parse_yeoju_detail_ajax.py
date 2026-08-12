"""
여주시도서관 상세페이지 내 비동기 소장처 조회 Ajax API 경로 규명
"""
from bs4 import BeautifulSoup

with open("yeoju_detail.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. script 태그 내 ajax 또는 json 호출 식별 ===")
for idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if any(w in txt for w in ["$.ajax", "ajax", "speciesKey", "bookKey"]):
        print(f"\nScript[{idx}]:")
        for line in txt.split("\n"):
            if any(w in line for w in ["url", "data", "success", "speciesKey", "bookKey", "post", "get"]):
                print("  ", line.strip()[:150])
