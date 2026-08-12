"""
부천시 HTML 내 fn_search 및 alpasq_redirect 정의 탐색
"""
from bs4 import BeautifulSoup

with open("bucheon_intro.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
print(f"Inline script tags: {len(scripts)}")

for i, sc in enumerate(scripts):
    txt = sc.text
    if any(w in txt for w in ["fn_search", "alpasq_redirect"]):
        print(f"\n=== Script[{i}] has fn_search / alpasq ===")
        idx = txt.find("function fn_search")
        if idx != -1:
            print(txt[idx:idx+800])
        else:
            idx2 = txt.find("alpasq_redirect")
            print(txt[max(0, idx2-150):idx2+600])
