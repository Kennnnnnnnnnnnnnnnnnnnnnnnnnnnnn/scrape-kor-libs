"""
화성시립도서관 스크래퍼
https://www.hscitylib.or.kr
- 전체 도서관을 대상으로 통합 검색합니다 (searchManageCodeArr 미지정).
"""
import requests
import urllib3
from bs4 import BeautifulSoup

from .base import LibraryScraper, BookInfo
from .registry import register_scraper

# 화성시 도서관 서버 SSL 인증서 이슈 → 경고 억제
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HwaseongScraper(LibraryScraper):
    """화성시립도서관 도서 검색"""

    def __init__(self):
        super().__init__(
            region_name="화성",
            base_url="https://www.hscitylib.or.kr/intro/menu/10003/program/30001/searchResultList.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        if author:
            params = {
                "searchType": "DETAIL",
                "searchAdvTitle": title,
                "searchAdvAuthor": author,
                "searchArticle": "SCORE",
                "searchOrder": "ASC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }
        else:
            params = {
                "searchType": "SIMPLE",
                "searchKeyword": title,
                "searchArticle": "SCORE",
                "searchOrder": "ASC",
                "searchManageCode": "ALL",
                "searchDisplay": "100",
            }

        all_books = []
        total_count = 0
        page = 1

        while True:
            params["currentPageNo"] = str(page)

            try:
                resp = requests.get(self.base_url, params=params, headers=self._headers, timeout=15, verify=False)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"  [오류] 화성 도서관 접속 실패: {e}")
                return total_count, all_books

            soup = BeautifulSoup(resp.text, "html5lib")

            # 총 검색 건수 (첫 페이지에서만 읽기)
            if page == 1:
                total_cnt_tag = soup.select_one("#totalCnt")
                if not total_cnt_tag:
                    total_cnt_tag = soup.select_one(
                        "#searchForm > div:nth-of-type(2) > div > div:nth-of-type(1) > div > span"
                    )
                total_count = int(total_cnt_tag.text.strip().replace(',', '')) if total_cnt_tag else 0
                if total_count == 0:
                    return 0, []

            # 도서 목록 파싱
            book_items = soup.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
            if not book_items:
                break

            path_data = "div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1)"

            for item in book_items:
                book = BookInfo(region="화성")

                title_tag = item.select_one(f"{path_data} > p > a")
                if title_tag:
                    book.title = title_tag.get("title", title_tag.text.strip())

                author_tag = item.select_one(f"{path_data} > ul > li:nth-of-type(1) > span:nth-of-type(1)")
                if author_tag:
                    book.author = author_tag.text.strip()

                dec_tag = item.select_one(f"{path_data} > ul > li:nth-of-type(3) > span:nth-of-type(1)")
                if dec_tag:
                    book.call_number = dec_tag.text.strip()

                sound_tag = item.select_one(f"{path_data} > ul > li:nth-of-type(3) > span:nth-of-type(2)")
                if sound_tag and "부록있음" in sound_tag.text:
                    book.has_audio = "O"

                loc_tag = item.select_one(f"{path_data} > ul > li:nth-of-type(4) > span")
                if loc_tag:
                    loc_text = loc_tag.text.strip()
                    book.location = loc_text
                    import re
                    match = re.search(r'\[(.+?)\]', loc_text)
                    if match:
                        lib_base = match.group(1).strip()
                        book.library = lib_base if lib_base.endswith("도서관") else lib_base + "도서관"
                    else:
                        book.library = loc_text

                all_books.append(book)

            # 다음 페이지 필요 여부
            if len(all_books) >= total_count:
                break
            page += 1

        return total_count, all_books


# 레지스트리에 등록
register_scraper("화성", HwaseongScraper)
