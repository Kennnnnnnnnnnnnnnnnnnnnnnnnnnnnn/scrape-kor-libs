"""
광명시도서관 DL/DD 상세 구조 분석 (Unicode 에러 우회용 파일 저장)
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

items = soup.select("div.list")
if items:
    prettified_html = items[0].select_one("dl").prettify()
    # 안전하게 파일로 써서 저장
    with open("gwangmyeong_dd_prettified.txt", "w", encoding="utf-8") as out:
        out.write(prettified_html)
    print("Saved to gwangmyeong_dd_prettified.txt successfully!")
else:
    print("No items found.")
