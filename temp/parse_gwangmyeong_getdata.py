"""
광명시도서관 getDataDetail 함수 본문 상세 덤프
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.select("script")
for i, sc in enumerate(scripts):
    txt = sc.text
    if "getDataDetail" in txt:
        print(f"=== Script[{i}] getDataDetail Definition ===")
        idx = txt.find("function getDataDetail")
        if idx != -1:
            # 안전하게 파일로 써서 저장
            with open("gwangmyeong_getdata_fn.txt", "w", encoding="utf-8") as out:
                out.write(txt[idx:idx+1500])
            print("Saved function definition to gwangmyeong_getdata_fn.txt")
            break
