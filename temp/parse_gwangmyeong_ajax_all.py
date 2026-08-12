"""
광명시도서관 HTML 내 AJAX 통신($.ajax 등) 비주석 구문 전수 탐색
"""
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    txt = f.read()

# $.ajax, $.post, $.get, .load( 패턴 탐색
matches = list(re.finditer(r"\$\.ajax|\$\.post|\$\.get|\.load\(", txt))
print(f"AJAX matches: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    # 인근 500바이트 덤프
    snippet = txt[max(0, pos-100):pos+400]
    # 주석 여부 확인
    is_comm = "/*" in txt[max(0, pos-400):pos] or "//" in txt[max(0, pos-100):pos]
    print(f"\nMatch {i} (Index {pos}, Commented: {is_comm}):")
    print("  ", snippet.strip().replace("\n", " "))
