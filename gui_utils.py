"""
GUI 팝업 및 파일 접근 예외 처리 유틸리티
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox


def show_error_and_exit(title: str, message: str):
    """
    오류 팝업창을 띄우고 프로그램을 안전하게 종료합니다.
    """
    try:
        root = tk.Tk()
        root.withdraw()  # 메인 윈도우 창 숨기기
        root.attributes("-topmost", True)  # 팝업을 최상단에 배치
        messagebox.showerror(title, message, parent=root)
        root.destroy()
    except Exception as e:
        print(f"[오류 팝업 출력 실패] {e}")
        print(f"[{title}] {message}")
    
    sys.exit(1)


def check_file_writable(file_path: str) -> bool:
    """
    파일이 현재 다른 프로그램에 의해 열려있거나 접근 불가능한 상태인지 체크합니다.
    파일이 열려있으면 팝업창을 띄우고 종료합니다.
    """
    if not os.path.exists(file_path):
        return True

    # 쓰기 전용 오픈 시도 (파일 잠금 여부 점검)
    try:
        with open(file_path, "r+", encoding="utf-8") as f:
            pass
        return True
    except PermissionError:
        file_name = os.path.basename(file_path)
        msg = (
            f"'{file_name}' 파일에 접근 권한이 거부되었습니다.\n\n"
            f"현재 엑셀(MS Excel)이나 다른 프로그램에서 이 파일이 열려있을 수 있습니다.\n"
            f"열려있는 엑셀 창을 완전히 닫은 후 다시 프로그램을 실행해 주세요.\n\n"
            f"파일 경로: {file_path}"
        )
        show_error_and_exit("엑셀 파일 접근 오류 (Permission Denied)", msg)
    except OSError as e:
        if getattr(e, 'errno', None) == 13:
            file_name = os.path.basename(file_path)
            msg = (
                f"'{file_name}' 파일이 잠겨 있거나 권한이 없습니다.\n"
                f"열려있는 엑셀 프로그램을 닫고 다시 실행해 주세요."
            )
            show_error_and_exit("엑셀 파일 접근 오류", msg)
        return True
    except Exception:
        return True

    return True
