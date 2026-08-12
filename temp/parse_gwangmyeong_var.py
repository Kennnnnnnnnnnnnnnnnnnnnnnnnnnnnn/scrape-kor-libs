"""
광명시도서관 HTML 내 dataDetail 전역 변수 선언부 추출
"""
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

# var dataDetail 또는 dataDetail = 형태 탐색
matches = list(re.finditer(r"dataDetail\s*=", html))
print(f"dataDetail matches: {len(matches)}")

for m in matches:
    pos = m.start()
    print("\n=== dataDetail match context ===")
    # 인근 2000바이트를 덤프
    snippet = html[pos:pos+2500]
    # 안전하게 파일로 써서 저장
    with open("gwangmyeong_datadetail_var.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Saved to gwangmyeong_datadetail_var.txt")
