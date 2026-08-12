"""
임시 파일 정리 및 temp 디렉토리 이동 스크립트
"""
import os
import shutil

ROOT_DIR = r"c:\__ken\proj_py\scrape-kor-libs"
TEMP_DIR = os.path.join(ROOT_DIR, "temp")

os.makedirs(TEMP_DIR, exist_ok=True)

KEEP_FILES = {
    "main.py", "main.spec", "gui_utils.py", "title_utils.py", "init_data_dir.py",
    "verify_summary.py", ".gitignore", "prompt-guide.md"
}

files = os.listdir(ROOT_DIR)

moved_count = 0
for f in files:
    file_path = os.path.join(ROOT_DIR, f)
    if os.path.isfile(file_path):
        if f in KEEP_FILES:
            continue
        
        # 임시 스크립트, html, txt, js, json, zip 파일 이동
        if (f.startswith("probe_") or f.startswith("parse_") or f.startswith("test_") 
                or f.startswith("debug_") or f.endswith(".html") or f.endswith(".txt") 
                or f.endswith(".js") or f.endswith(".json") or f.endswith(".zip")):
            try:
                shutil.move(file_path, os.path.join(TEMP_DIR, f))
                moved_count += 1
                print(f"이동됨: {f} -> temp/{f}")
            except Exception as e:
                print(f"오류 ({f}): {e}")

print(f"\n총 {moved_count}개 임시 파일 temp/ 디렉토리로 이동 완료.")
