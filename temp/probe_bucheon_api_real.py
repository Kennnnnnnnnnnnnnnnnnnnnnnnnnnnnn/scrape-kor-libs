"""
bucheon_app.js 내 /api/search 호출 코드 파싱
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("bucheon_app.js", "r", encoding="utf-8") as f:
    js = f.read()

idx = js.find('"/api/search"')
if idx == -1:
    idx = js.find("'/api/search'")

if idx != -1:
    print("=== /api/search code snippet ===")
    print(js[max(0, idx-300):min(len(js), idx+300)])

matches = re.finditer(r'url\s*:\s*["\']/api/search["\']', js)
for m in matches:
    print("\n=== Found url: /api/search ===")
    print(js[max(0, m.start()-200):min(len(js), m.end()+200)])
