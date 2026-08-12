"""사용되지 않는 엑셀 파일 찾아 삭제"""
import os
from pathlib import Path
from scrapers.registry import METRO_MAP

DATA_DIR = Path("data")

# METRO_MAP에 등록된 유효한 (광역, 지역) 조합 수집
valid_names = set()
for metro, regions in METRO_MAP.items():
    for r in regions:
        valid_names.add((metro, r))

unused = []
for metro_dir in DATA_DIR.iterdir():
    if not metro_dir.is_dir():
        continue
    for f in metro_dir.glob("*.xlsx"):
        if f.name.startswith("~$"):
            continue
        region = f.stem.strip()
        if (metro_dir.name, region) not in valid_names:
            unused.append(str(f))

print(f"총 미사용 엑셀 파일: {len(unused)}개")
for u in unused:
    print(f"  삭제: {u}")
    os.remove(u)
print("완료!")
