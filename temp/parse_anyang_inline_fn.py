"""
안양시립 HTML 내 fnCollectionInfo 함수 정의 탐색
"""
from bs4 import BeautifulSoup

with open("anyang_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
print(f"Inline script tags: {len(scripts)}")

for i, sc in enumerate(scripts):
    txt = sc.text
    if "fnCollectionInfo" in txt:
        print(f"\n=== Script[{i}] has fnCollectionInfo ===")
        # 함수 시작 부근 탐색
        idx = txt.find("function fnCollectionInfo")
        if idx != -1:
            print(txt[idx:idx+800])
        else:
            print("fnCollectionInfo word exists, but not function definition. Snippet:")
            idx2 = txt.find("fnCollectionInfo")
            print(txt[max(0, idx2-150):idx2+600])
