"""
gunpo_main.js 내 pyxis-api 호출 코드 파싱
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js_text = f.read()

print("JS length:", len(js_text))

matches = re.findall(r'.{0,100}pyxis-api.{0,100}', js_text)
print(f"pyxis-api matches count: {len(matches)}")
for i, m in enumerate(matches[:15]):
    print(f"[{i}] {m.strip()}")
