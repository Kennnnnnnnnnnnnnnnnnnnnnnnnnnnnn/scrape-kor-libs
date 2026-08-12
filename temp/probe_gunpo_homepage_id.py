"""
gunpo_main_real.js에서 HOME_PAGE_ID 선언부 탐색
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("gunpo_main_real.js", "r", encoding="utf-8") as f:
    js = f.read()

matches = re.finditer(r'HOME_PAGE_ID\s*:\s*([0-9]+)', js)
for m in matches:
    print(f"HOME_PAGE_ID: {m.group(1)} at {m.start()}")
    print(" ", js[max(0, m.start()-100):min(len(js), m.end()+100)])

matches2 = re.finditer(r'API_URL\s*:\s*["\']([^"\']+)["\']', js)
for m in matches2:
    print(f"API_URL: {m.group(1)} at {m.start()}")

matches3 = re.finditer(r'\.constant\s*\(\s*["\']CONFIG["\']\s*,\s*(\{.*?\})\s*\)', js)
for m in matches3:
    print("Found CONFIG constant definition!")
    print(" ", m.group(1)[:300])
