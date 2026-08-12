"""
의정부 상세페이지 전체 스크립트 파일 저장 및 정밀 분석
"""
from bs4 import BeautifulSoup

with open("uijeongbu_detail.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

with open("uijeongbu_all_scripts.txt", "w", encoding="utf-8") as out:
    for idx, sc in enumerate(soup.select("script")):
        src = sc.get("src")
        txt = sc.text.strip()
        out.write(f"\n======================================================\n")
        out.write(f"Script[{idx}] src='{src}'\n")
        out.write(f"======================================================\n")
        if txt:
            out.write(txt + "\n")
print("Saved to uijeongbu_all_scripts.txt successfully!")
