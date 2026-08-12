"""
안양시립도서관 스크래퍼 (XHR 기반 실시간 청구기호/지점 소장정보 연동 구현)
"""
import requests
from bs4 import BeautifulSoup
import re
from .jnet import JnetTypeAScraper, _fetch, _SslAdapter
from .registry import register_scraper
from .base import BookInfo

class AnyangScraper(JnetTypeAScraper):
    """안양시립도서관 실시간 검색 스크래퍼 (1차 검색 후 2차 XHR 소장정보 연동)"""

    def __init__(self):
        super().__init__(
            region_name="안양시",
            domain="lib.anyang.go.kr",
            site_code="intro",
            menu_id="",
            program_id="",
            use_ssl_adapter=True
        )
        self.base_url = "https://lib.anyang.go.kr/intro/searchResultList.do"

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        if author:
            params = {
                "searchType": "DETAIL",
                "searchAdvTitle": title,
                "searchAdvAuthor": author,
                "searchManageCode": "ALL",
                "searchAdvContentsType": "ALL",
                "searchAdvTextLang": "ALL",
                "searchArticle": "SCORE",
                "searchOrder": "ASC"
            }
        else:
            params = {
                "searchType": "SIMPLE",
                "searchKeyword": title,
                "searchManageCode": "ALL",
                "topSearchCondition": "ALL",
                "searchArticle": "SCORE",
                "searchOrder": "ASC"
            }

        try:
            # SSL 우회하여 직접 1차 검색 fetch
            resp = _fetch(self.base_url, params, self._headers, use_ssl_adapter=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 안양 도서관 1차 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html5lib")

        from .jnet import _parse_int
        total_cnt_tag = soup.select_one("#totalCnt")
        total_count = _parse_int(total_cnt_tag.text) if total_cnt_tag else 0

        if total_count == 0:
            return 0, []

        book_items = soup.select("#bookList li")
        if not book_items:
            book_items = soup.select(".bookArea")

        books = []
        # 성능 및 트래픽 보전을 위해 최대 10건까지만 2차 XHR 조회 진행
        for item in book_items[:10]:
            area = item.select_one(".bookArea") or item
            
            # 1. 1차 정보 파싱
            title_tag = area.select_one("a.book_name")
            if not title_tag:
                continue
            
            base_title = title_tag.text.strip()
            
            # 저자
            base_author = ""
            info_items = area.select("ul.dot-list > li")
            for info in info_items:
                text = info.text.strip()
                if "저자" in text:
                    base_author = text.replace("저자 :", "").replace("저자:", "").replace("저자", "").replace(":", "").strip()
                    break

            # 2. XHR 파라미터 (speciesKey, pubFormCode) 추출
            # btn_haveInfo 또는 btn_sergeInfo 의 onclick 속성에서 획득
            # 예: fnCollectionInfo('1', '20156253,20156256,...', 'MO');
            species_key = ""
            pub_form_code = "MO"
            
            have_btn = area.select_one(".btn_haveInfo")
            if have_btn:
                onclick = have_btn.get("onclick", "")
                m = re.search(r"fnCollectionInfo\(\s*'[^']*'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)", onclick)
                if m:
                    species_key = m.group(1).strip()
                    pub_form_code = m.group(2).strip()

            if not species_key:
                # onclick="fnDetail('20156253,...', '979116...', 'MO')" 형태도 탐색
                name_btn = area.select_one("a.book_name")
                if name_btn:
                    onclick = name_btn.get("onclick", "")
                    m = re.search(r"fnDetail\(\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*\)", onclick)
                    if m:
                        species_key = m.group(1).strip()
                        pub_form_code = m.group(3).strip()

            # 3. 2차 XHR로 상세 소장정보 요청
            lib_info_list = []
            if species_key:
                xhr_url = "https://lib.anyang.go.kr/search/include/collectionBookList.do"
                xhr_data = {"speciesKey": species_key, "pubFormCode": pub_form_code}
                try:
                    # SSL 세션 유지
                    xhr_resp = _fetch(xhr_url, xhr_data, self._headers, use_ssl_adapter=True)
                    if xhr_resp.status_code == 200:
                        xsoup = BeautifulSoup(xhr_resp.text, "html.parser")
                        rows = xsoup.select("table tbody tr")
                        for row in rows:
                            tds = row.select("td")
                            if len(tds) >= 6:
                                lib_name = tds[0].text.strip()
                                call_no = tds[3].text.replace("청구기호", "").replace("인쇄", "").strip()
                                shelf_loc = tds[5].text.strip()
                                lib_info_list.append((lib_name, call_no, shelf_loc))
                except Exception as e:
                    pass

            # 4. 개별 소장 도서관별 BookInfo 생성 분리
            if lib_info_list:
                for lib, call, loc in lib_info_list:
                    book = BookInfo(region="경기도")
                    book.title = base_title
                    book.author = base_author
                    book.library = lib + "도서관" if not lib.endswith("도서관") else lib
                    book.call_number = call
                    book.location = loc
                    
                    if book.library.startswith("안양 "):
                        book.library = book.library.replace("안양 ", "")
                    if "도서관도서관" in book.library:
                        book.library = book.library.replace("도서관도서관", "도서관")
                        
                    books.append(book)
            else:
                # 2차 XHR 실패 또는 소장정보 없을 시 1차 정보 기반 1건 생성 fallback
                book = BookInfo(region="경기도")
                book.title = base_title
                book.author = base_author
                book.library = "안양시립도서관"
                book.call_number = ""
                books.append(book)

        return total_count, books

# 레지스트리 등록
register_scraper("안양", AnyangScraper, metro_name="경기도")
register_scraper("안양시", AnyangScraper, metro_name="경기도")
register_scraper("안양시립도서관", AnyangScraper, metro_name="경기도")
