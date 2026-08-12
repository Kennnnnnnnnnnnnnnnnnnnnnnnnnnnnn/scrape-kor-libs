"""
시흥시 main.js 내 CONFIG 주입 변수(a)의 실제 선언부 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

pos = txt.find('constant("CONFIG"')
if pos != -1:
    print(f"Found constant('CONFIG') at pos: {pos}")
    # 직전 1500바이트 덤프
    snippet = txt[max(0, pos-1500):pos+50]
    print("\n=== Pre-constant Area ===")
    print(snippet.strip().replace("\n", " "))
else:
    print("constant('CONFIG') not found!")
