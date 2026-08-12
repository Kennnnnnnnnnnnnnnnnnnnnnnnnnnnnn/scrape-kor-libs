"""
GenericLibraryScraper 기반 미구현 스크래퍼 정밀 구분
"""
import scrapers
from scrapers.registry import METRO_MAP, get_scraper
from scrapers.generic import GenericLibraryScraper
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Registered Scrapers Summary (Precision) ===")
total_cnt = 0
generic_cnt = 0
real_cnt = 0

unimplemented_by_metro = {}

for metro, region_list in sorted(METRO_MAP.items()):
    unimplemented_by_metro[metro] = []
    print(f"\n[{metro}] ({len(region_list)} 개 도서관):")
    for reg in sorted(region_list):
        scr = get_scraper(reg, metro)
        cls_name = scr.__class__.__name__
        is_generic = isinstance(scr, GenericLibraryScraper)
        total_cnt += 1
        if is_generic:
            generic_cnt += 1
            unimplemented_by_metro[metro].append(reg)
            print(f"  ❌ {reg}: {cls_name} (미구현)")
        else:
            real_cnt += 1
            print(f"  ✅ {reg}: {cls_name}")

print("\n" + "="*50)
print(f"총 지원 도서관 수: {total_cnt}")
print(f"실시간 수집 연동 완료 (Real): {real_cnt}")
print(f"미구현 도서관 (Generic Fallback): {generic_cnt}")
print("="*50)

print("\n=== 미구현 도서관 (우선 구현 대상) ===")
for metro, libs in unimplemented_by_metro.items():
    if libs:
        print(f"\n[{metro}] ({len(libs)}개): {', '.join(libs)}")
