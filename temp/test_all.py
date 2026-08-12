"""
112개 전체 공공도서관 엑셀 파일 및 스크래퍼 통합 테스트 스크립트
"""
import os
import sys
from pathlib import Path
import openpyxl

from scrapers import get_scraper, find_metro_by_region, METRO_MAP


def run_full_test():
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"

    print("=" * 70)
    print(" [TEST] 전국 공공도서관 엑셀 파일 및 스크래퍼 100% 전수 테스트")
    print("=" * 70)

    # 1. 목록상의 전체 도서관 개수 산출
    total_requested_libs = sum(len(libs) for libs in METRO_MAP.values())
    print(f" [INFO] 목록 정의 도서관 총 개수: {total_requested_libs}개")

    # 2. data/ 폴더 내 생성된 엑셀 파일 검사
    created_excel_files = list(data_dir.glob("**/*.xlsx"))
    created_excel_files = [f for f in created_excel_files if not f.name.startswith("~$")]
    print(f" [INFO] data/ 하위 생성된 엑셀 파일 개수: {len(created_excel_files)}개")

    success_count = 0
    fail_count = 0

    print("\n--- 각 광역단위별 엑셀 파일 및 스크래퍼 검증 진행 ---")

    for metro_name, lib_list in METRO_MAP.items():
        metro_dir = data_dir / metro_name
        print(f"\n[광역단위: {metro_name}] ({len(lib_list)}개 도서관)")

        for lib_name in lib_list:
            excel_path = metro_dir / f"{lib_name}.xlsx"

            # 특수 케이스 파일명 처리 (예: 화성.xlsx, 부산.xlsx, 용인.xlsx, 안양.xlsx 등)
            if not excel_path.exists():
                short_name = lib_name.replace("시", "").replace("군", "")
                alt_path = metro_dir / f"{short_name}.xlsx"
                if alt_path.exists():
                    excel_path = alt_path

            if not excel_path.exists():
                print(f"  [FAIL] [{lib_name}] 엑셀 파일 없음: {excel_path}")
                fail_count += 1
                continue

            try:
                # 엑셀 파일 열기 검증
                wb = openpyxl.load_workbook(str(excel_path))
                if '입력' not in wb.sheetnames:
                    print(f"  [FAIL] [{lib_name}] '입력' 시트 없음")
                    fail_count += 1
                    continue

                # 스크래퍼 인스턴스화 및 테스트
                scraper = get_scraper(lib_name, metro_name)
                total_cnt, books = scraper.search("파이썬 코딩", "")

                print(f"  [OK] [{lib_name}] 엑셀 존재 및 스크래퍼 정상 동작 (검색 결과: {total_cnt}건)")
                success_count += 1

            except Exception as e:
                print(f"  [FAIL] [{lib_name}] 검증 에러: {e}")
                fail_count += 1

    print("\n" + "=" * 70)
    print(f" [SUMMARY] 최종 테스트 결과:")
    print(f"  - 성공: {success_count} / {total_requested_libs}개 도서관 ({(success_count/total_requested_libs)*100:.1f}%)")
    print(f"  - 실패: {fail_count}개")
    print("=" * 70)


if __name__ == "__main__":
    run_full_test()
