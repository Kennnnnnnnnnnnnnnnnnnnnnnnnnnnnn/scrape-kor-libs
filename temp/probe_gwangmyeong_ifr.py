with open("gwangmyeong_search.html", "r", encoding="utf-8") as f:
    txt = f.read()

print("Iframe exists:", "iframe" in txt)
print("Iframe count:", txt.count("iframe"))

# iframe src 속성 출력
from bs4 import BeautifulSoup
soup = BeautifulSoup(txt, "html.parser")
ifrs = soup.select("iframe")
for ifr in ifrs:
    print("  Iframe Src:", ifr.get("src"))
