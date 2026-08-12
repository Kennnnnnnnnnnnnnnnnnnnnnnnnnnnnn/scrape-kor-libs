"""
data/ 디렉터리 및 광역단위 엑셀 파일 구조 생성 스크립트
"""
import os
import shutil
from pathlib import Path
import openpyxl

from scrapers.registry import METRO_MAP, find_metro_by_region


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def setup_data_directory():
    """
    data/ 디렉터리 및 광역단위 폴더를 생성하고
    기존 엑셀 파일 이동 및 광역단위별 지역 엑셀 파일 템플릿을 생성합니다.
    """
    DATA_DIR.mkdir(exist_ok=True)

    # 1. 광역단위 폴더 생성
    for metro_name in METRO_MAP.keys():
        metro_dir = DATA_DIR / metro_name
        metro_dir.mkdir(exist_ok=True)

    # 2. 루트에 있는 기존 엑셀 파일 이동
    old_files = ["부산.xlsx", "안양.xlsx", "용인.xlsx", "제주.xlsx", "화성.xlsx"]
    for fname in old_files:
        src = BASE_DIR / fname
        if src.exists():
            stem = src.stem
            metro_name = find_metro_by_region(stem)
            dest_dir = DATA_DIR / metro_name
            dest_dir.mkdir(exist_ok=True)
            dest_file = dest_dir / fname
            if not dest_file.exists():
                shutil.move(str(src), str(dest_file))
                print(f"[이동] {fname} -> data/{metro_name}/{fname}")
            else:
                os.remove(str(src))

    # 3. 모든 광역단위의 지역/도서관별 기본 샘플 엑셀 파일 배치
    for metro_name, lib_list in METRO_MAP.items():
        metro_dir = DATA_DIR / metro_name
        metro_dir.mkdir(exist_ok=True)

        for lib_name in lib_list:
            # 엑셀 파일 이름 정제
            file_name = f"{lib_name}.xlsx"
            target_path = metro_dir / file_name

            if not target_path.exists():
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "입력"
                # 샘플 입력 데이터 헤더
                ws.append(["책 이름", "저자"])
                ws.append(["파이썬 코딩", "홍길동"])
                ws.append(["공공도서관 검색 안내", ""])
                wb.save(target_path)

    print("[완료] data/ 광역단위 디렉터리 및 엑셀 파일 구조 생성이 완료되었습니다.")


if __name__ == "__main__":
    setup_data_directory()
