"""
시흥시 main.js 내 인라인 병합된 JSON 설정 데이터 추출
"""
with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

import re

# define("json!_conf/settings/api.json", [], function() { return { ... } }) 형태
# 혹은 define("json!_conf/settings/api.json", {...}) 형태 매칭
targets = ["api.json", "search.json", "default.json"]
for t in targets:
    print(f"\n=== Search merged JSON: {t} ===")
    matches = list(re.finditer(f'define\\("json!_conf/settings/{t}"', txt))
    if not matches:
        matches = list(re.finditer(f'"json!_conf/settings/{t}"', txt))
    
    for m in matches[:5]:
        pos = m.start()
        print(txt[pos:pos+1500].strip().replace("\n", " "))
