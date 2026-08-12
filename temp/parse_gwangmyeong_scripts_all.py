"""
광명시도서관 HTML 내 모든 인라인 스크립트 내용 분석
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
print(f"Total script tags: {len(scripts)}")

for i, sc in enumerate(scripts):
    src = sc.get("src")
    txt = sc.text.strip()
    if src:
        print(f"[{i}] Script Src: {src}")
    elif txt:
        # 인라인 스크립트
        # 길이 및 내용 앞머리 출력
        print(f"[{i}] Inline Script (Length: {len(txt)}):")
        # 줄 수가 작으면 전체 출력, 길면 앞/뒤 200바이트만 출력
        lines = txt.split("\n")
        if len(lines) < 25:
            print("  Full Context:")
            for line in lines:
                print("    ", line.strip()[:150])
        else:
            print("  Snippet (Head):")
            for line in lines[:8]:
                print("    ", line.strip()[:150])
            print("  ...")
            print("  Snippet (Tail):")
            for line in lines[-8:]:
                print("    ", line.strip()[:150])
