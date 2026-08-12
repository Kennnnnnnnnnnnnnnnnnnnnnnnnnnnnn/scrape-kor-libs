"""
시흥시 main.js 내 CONFIG 상수의 변수 a의 값 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

pos = txt.find('constant("CONFIG",a)')
if pos != -1:
    print("=== CONFIG Constant Context ===")
    # 그 전의 1500바이트 출력
    print(txt[max(0, pos-1500):pos+50].strip().replace("\n", " "))
else:
    print("constant not found")
