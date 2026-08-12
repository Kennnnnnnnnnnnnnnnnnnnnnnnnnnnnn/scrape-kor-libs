"""
유성구립도서관 결과 본문 영역 추출 스크립트
"""
from bs4 import BeautifulSoup

with open("yuseong_brief_2.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 본문 영역
content = soup.select_one("#content") or soup.select_one(".content") or soup.select_one("main")
if not content:
    # sub_content 같은 대체 요소
    for div in soup.select("div"):
        cls = div.get("class", [])
        if any("content" in c for c in cls):
            content = div
            break

if content:
    print(f"Content found! tag={content.name} class={content.get('class')}")
    # 파일로 저장해서 직접 보기
    with open("yuseong_content.html", "w", encoding="utf-8") as out:
        out.write(content.prettify())
    print("yuseong_content.html saved successfully.")
    
    # 텍스트 단어 빈도
    print("\n=== TEXT SCAN ===")
    text = content.text
    for word in ["파이썬", "저자", "청구", "출판", "건", "결과"]:
        print(f"Word '{word}' count: {text.count(word)}")
else:
    print("Content not found!")
