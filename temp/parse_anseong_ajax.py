"""
안성시 biblioSearch JS 함수 분석
"""
import requests
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("anseong_search_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

for sc in soup.select("script"):
    txt = sc.text
    if "biblioSearch" in txt:
        print("=== biblioSearch script found ===")
        lines = txt.split("\n")
        for idx, line in enumerate(lines):
            if "biblioSearch" in line or "ajax" in line.lower() or "url" in line.lower():
                print(f"  Line {idx}: {line.strip()[:150]}")
