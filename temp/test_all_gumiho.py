"""
전국 109개 도서관 '구미호식당' 키워드 전수 검증 (실시간 출력 버퍼링 해제 버전)
"""
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import scrapers
from scrapers.registry import METRO_MAP, get_scraper

print("==================================================", flush=True)
print("  전국 109개 공공도서관 '구미호식당' 실시간 전수 검증", flush=True)
print("==================================================\n", flush=True)

KEYWORD = "구미호식당"
total_count = 0
success_count = 0
failed_libraries = []

start_time = time.time()

for metro, regions in METRO_MAP.items():
    print(f"\n[{metro}] ({len(regions)}개 도서관)", flush=True)
    for reg in regions:
        total_count += 1
        try:
            scraper = get_scraper(reg, metro)
            cnt, books = scraper.search(KEYWORD)
            
            if cnt > 0 or len(books) > 0:
                success_count += 1
                sample_book = books[0].title if books else "도서 리스트 확인됨"
                sample_lib = books[0].library if books else reg
                print(f"  ✅ [{reg}] -> {cnt}건 수집 성공 (예: {sample_book[:30]} | {sample_lib})", flush=True)
            else:
                print(f"  ⚠️ [{reg}] -> 0건 수집", flush=True)
                failed_libraries.append((metro, reg, "0건 수집"))
        except Exception as e:
            err_msg = f"{type(e).__name__}: {e}"
            print(f"  ❌ [{reg}] -> 오류 발생: {err_msg[:60]}", flush=True)
            failed_libraries.append((metro, reg, err_msg))

elapsed = time.time() - start_time
print("\n==================================================", flush=True)
print(f"  전수 검증 완료! (소요 시간: {elapsed:.2f}초)", flush=True)
print(f"  총 도서관 수: {total_count}", flush=True)
print(f"  성공/수집 확인: {success_count} 개 ({success_count/total_count*100:.1f}%)", flush=True)
print(f"  확인 필요/오류: {len(failed_libraries)} 개", flush=True)
print("==================================================", flush=True)

if failed_libraries:
    print("\n[확인 및 디버깅 필요 대상]", flush=True)
    for m, r, err in failed_libraries:
        print(f"  - {m} {r}: {err}", flush=True)
