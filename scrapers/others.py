"""
전국 광역단위 공공도서관 (부산, 대구, 인천, 광주, 대전, 울산, 세종, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주) 스크래퍼 등록 모듈
- 기존 개별 스크래퍼(busan.py, jeju.py)가 있는 도서관은 중복 등록 제외
- jnet 엔드포인트 확인된 도서관 (유성구립도서관, 논산시립도서관 등) 실제 등록
- 울산도서관: 실시간 검색 API 연동 추가
- 나머지는 GenericLibraryScraper (미구현, 빈 결과 반환)
"""
import re
import requests
from bs4 import BeautifulSoup

from .registry import register_scraper, METRO_MAP
from .jnet import JnetTypeAScraper, _fetch, _SslAdapter
from .generic import GenericLibraryScraper
from .base import LibraryScraper, BookInfo

# 이미 개별 파일로 구현된 도서관 (busan.py, jeju.py, incheon.py 등에서 등록)
ALREADY_REGISTERED = {"부산도서관", "제주도립도서관", "한라도서관", "우당도서관", "탐라도서관", "제주시기적의도서관", "애월도서관", "조천읍도서관", "한경도서관", "삼매봉도서관", "중앙도서관", "동부도서관", "서부도서관", "서귀포기적의도서관", "성산일출도서관", "안덕산방도서관", "표선도서관", "꿈바당어린이도서관", "인천광역시교육청도서관", "청주시립도서관", "순천시립도서관", "전주시립도서관", "군산시립도서관", "천안시도서관", "김해시립도서관", "창원시립도서관", "구미시립도서관", "포항시립도서관", "목포시립도서관", "여수시립도서관", "전라남도립도서관", "아산시립도서관", "충청남도도서관", "논산시립도서관", "충주시립도서관", "제천시립도서관", "익산시립도서관", "대구광역시립도서관통합포털", "광주광역시립도서관", "한밭도서관", "세종특별자치시립도서관", "춘천시립도서관", "원주시립도서관", "경상남도대표도서관"}


# ========================================================================
# 충북 청주시립도서관 (library.cheongju.go.kr)
# ========================================================================

class CheongjuScraper(LibraryScraper):
    """충북 청주시립도서관 스크래퍼 (library.cheongju.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="청주시립도서관",
            base_url="https://library.cheongju.go.kr/lib/dls_le/index.php"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query,
            "manageCode": ""
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.cheongju.go.kr/lib/front/index.php'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 청주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

        cnt_tag = soup.select_one("span.total, span.num, strong.count, div.total")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.divList > div.list")
        books = []
        for item in items:
            tit_tag = item.select_one("dt a, div.ico a")
            if tit_tag:
                book_title = tit_tag.text.strip()
            else:
                txt_full = item.text.strip()
                lines = [l.strip() for l in txt_full.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title:
                continue

            lib_el = item.select_one("li.so span.blue, li.so span")
            lib_name = lib_el.get_text(strip=True) if lib_el else "청주시립도서관"

            status_el = item.select_one("ol strong")
            status_text = status_el.get_text(strip=True) if status_el else ""
            is_available = ("대출가능" in status_text) or ("가능" in status_text)

            book = BookInfo(region="충청북도")
            book.title = book_title
            book.library = lib_name if lib_name else "청주시립도서관"
            book.available = is_available
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("청주시립도서관", CheongjuScraper, metro_name="충청북도")






# ========================================================================
# 전북 전주시립도서관 (lib.jeonju.go.kr)
# ========================================================================

class JeonjuScraper(LibraryScraper):
    """전북 전주시립도서관 스크래퍼 (lib.jeonju.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="전주시립도서관",
            base_url="https://lib.jeonju.go.kr/index.jeonju"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menuCd": "DOM_000000103002000000",
            "searchKeyword": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.jeonju.go.kr/index.jeonju'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 전주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.total, span.num, strong.count")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("ul.result_list > li, table tbody tr, div.search_list_box, li.search_item")
        books = []
        for item in items:
            tit_tag = item.select_one("a.title, td.title a, dt.tit a, span.title")
            if tit_tag:
                book_title = tit_tag.text.strip()
            else:
                txt_full = item.text.strip()
                lines = [l.strip() for l in txt_full.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")

            book_author = ""
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            if m_auth:
                book_author = m_auth.group(1).strip()

            lib_name = "전주시립도서관"
            m_lib = re.search(r"\[([^\]]+도서관)\]", txt)
            if m_lib:
                lib_name = m_lib.group(1).strip()

            call_no = ""
            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            if m_call:
                call_no = m_call.group(1).strip()

            book = BookInfo(region="전북특별자치도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("전주시립도서관", JeonjuScraper, metro_name="전북특별자치도")


# ========================================================================
# 전북 군산시립도서관 (lib.gunsan.go.kr - JNET 연동)
# ========================================================================

class GunsanScraper(LibraryScraper):
    """전북 군산시립도서관 스크래퍼 (lib.gunsan.go.kr - JNET)"""
    def __init__(self):
        super().__init__(
            region_name="군산시립도서관",
            base_url="https://lib.gunsan.go.kr/web/menu/10003/program/30001/searchResultList.do"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchType": "SIMPLE",
            "searchCategory": "ALL",
            "searchKey": "ALL",
            "searchLibrary": "ALL",
            "searchKeyword": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.gunsan.go.kr/web/index.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 군산시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("div.book_dataInner")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, span.tit")
            if tit_tag:
                book_title = tit_tag.text.strip()
            else:
                txt_full = item.text.strip()
                m_tit = re.search(r"단행본\s+([^\n\r]+)", txt_full)
                book_title = m_tit.group(1).strip() if m_tit else ""

            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")

            book_author = ""
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            if m_auth:
                book_author = m_auth.group(1).strip()

            lib_name = "군산시립도서관"
            m_lib = re.search(r"\[([^\]]+)\]", txt)
            if m_lib:
                raw_lib = m_lib.group(1).strip()
                if raw_lib == "공":
                    lib_name = "군산시립도서관"
                else:
                    lib_name = raw_lib if raw_lib.endswith("도서관") or "자료실" in raw_lib else raw_lib + "도서관"

            call_no = ""
            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            if m_call:
                call_no = m_call.group(1).strip()

            book = BookInfo(region="전북특별자치도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("군산시립도서관", GunsanScraper, metro_name="전북특별자치도")


# ========================================================================
# 충남 천안시도서관 (kolas.cheonan.go.kr - KOLAS/DLS 연동)
# ========================================================================

class CheonanScraper(LibraryScraper):
    """충남 천안시도서관 스크래퍼 (kolas.cheonan.go.kr & elib.cheonan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="천안시도서관",
            base_url="https://kolas.cheonan.go.kr/search/index.php"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        books = []
        total_count = 0

        # 1. KOLAS DLS (종이도서관)
        params_k = {
            "mod": "wdDataSearch",
            "act": "searchIList",
            "item": "total",
            "word": query,
            "manageCode": ""
        }
        headers_k = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://kolas.cheonan.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params_k, headers=headers_k, timeout=12, verify=False)
            r.raise_for_status()
            soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")

            cnt_tag = soup.select_one("span.total, span.num, strong.count, div.total")
            if cnt_tag:
                m = re.search(r"\d+", cnt_tag.text.strip())
                if m:
                    total_count = int(m.group(0))

            items = soup.select("div.divList > div.list")
            for item in items:
                tit_tag = item.select_one("div.ico a") or item.select_one("dt a") or item.select_one("a[href*='searchResultDetail']")
                book_title = ""
                if tit_tag:
                    book_title = tit_tag.get_text(strip=True)
                    if not book_title and tit_tag.find('img'):
                        book_title = tit_tag.find('img').get('alt', '')
                        book_title = re.sub(r'<[^>]+>', '', book_title).strip()

                if not book_title:
                    txt_full = item.text.strip()
                    lines = [l.strip() for l in txt_full.split("\n") if l.strip()]
                    book_title = lines[0] if lines else ""

                if not book_title:
                    continue

                lib_el = item.select_one("li.so span.blue") or item.select_one("li.so span")
                lib_name = lib_el.get_text(strip=True) if lib_el else "천안시도서관"

                status_el = item.select_one("ol strong")
                status_text = status_el.get_text(strip=True) if status_el else ""
                is_available = ("대출가능" in status_text) or ("가능" in status_text)

                book = BookInfo(region="충청남도")
                book.title = book_title
                book.library = lib_name if lib_name else "천안시도서관"
                book.available = is_available
                books.append(book)
        except Exception as e:
            print(f"  [오류] 천안시도서관 KOLAS 검색 실패: {e}")

        # 2. FxLibrary (전자도서관) - 병행 수집
        try:
            url_e = "https://elib.cheonan.go.kr/FxLibrary/product/list/"
            params_e = {
                'category': 'book',
                'searchoption': '1',
                'searchType': 'search',
                'keyword': query
            }
            headers_e = {
                'User-Agent': self._headers['User-Agent'],
                'Referer': 'https://elib.cheonan.go.kr/FxLibrary/'
            }
            r_e = self._session.get(url_e, params=params_e, headers=headers_e, timeout=10, verify=False)
            if r_e.status_code == 200:
                soup_e = BeautifulSoup(r_e.content.decode('utf-8', 'ignore'), "html.parser")
                e_items = soup_e.select(".book_list li, div.book_box, ul.list_type_box > ul > li")
                for item in e_items:
                    tit_tag = item.select_one(".title, a.book_title, dt a, p.tit")
                    if tit_tag:
                        b_title = tit_tag.get_text(strip=True)
                        if b_title:
                            book = BookInfo(region="충청남도")
                            book.title = b_title
                            book.library = "천안시전자도서관"
                            book.available = True
                            books.append(book)
        except Exception as e:
            pass

        final_total = max(total_count, len(books))
        return final_total, books

for name in ["천안시도서관", "천안시립도서관", "천안도서관", "천안시전자도서관", "천안전자도서관"]:
    register_scraper(name, CheonanScraper, metro_name="충청남도")




# ========================================================================
# 경남 김해시립도서관 (libbook.gimhae.go.kr)
# ========================================================================

class GimhaeScraper(LibraryScraper):
    """경남 김해시립도서관 스크래퍼 (libbook.gimhae.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="김해시립도서관",
            base_url="http://libbook.gimhae.go.kr:8080/search/list.do"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "searchKeyword": query,
            "title": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.gimhae.go.kr/main.web'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 김해시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.total, span.num, strong.count")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("ul.result_list > li, table tbody tr, div.search_list_box, li.search_item")
        books = []
        for item in items:
            tit_tag = item.select_one("a.title, td.title a, dt.tit a, span.title")
            if tit_tag:
                book_title = tit_tag.text.strip()
            else:
                txt_full = item.text.strip()
                lines = [l.strip() for l in txt_full.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")

            book_author = ""
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            if m_auth:
                book_author = m_auth.group(1).strip()

            lib_name = "김해시립도서관"
            m_lib = re.search(r"\[([^\]]+도서관)\]", txt)
            if m_lib:
                lib_name = m_lib.group(1).strip()

            call_no = ""
            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            if m_call:
                call_no = m_call.group(1).strip()

            book = BookInfo(region="경상남도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("김해시립도서관", GimhaeScraper, metro_name="경상남도")


# ========================================================================
# ========================================================================
# 경남 창원시립도서관 (lib.changwon.go.kr)
# ========================================================================

class ChangwonScraper(LibraryScraper):
    """경남 창원시립도서관 스크래퍼 (lib.changwon.go.kr - JSON API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="창원시립도서관",
            base_url="https://lib.changwon.go.kr/book/data2.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.changwon.go.kr/book/search.php'
        }
        manage_codes = "MA,MB,MC,MD,ME,MG,MH,MJ,MK,MM,MN,MO,MP,PA,PB,PC,PD,PE,PF,PG,PH,PI,PJ,PK,PL,PM,PN,PO,PP,PQ,PR,PS,PT,PU,PV,PW,PX,PY,PZ,SA,SB,SC,SD,SE,SF,SG,SH,SI,SJ,SK,SL,SM,TA,TB,TC,TD,TE,TF,TG,TH,TI,TJ,TK,TL,TM,TN,TO,TP,TQ,TR,TS,TT,TU,TV,TW,TX,TY,TZ,UA,UB"

        all_books = []
        total_count = 0
        page = 1
        display_num = 100

        while True:
            params = {
                "search_txt": query,
                "manage_code": manage_codes,
                "lib_code": "cl",
                "search_type": "normal",
                "pageno": page,
                "display": display_num
            }

            try:
                r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  [오류] 창원시립도서관 검색 실패: {e}")
                return total_count, all_books

            api_resp = data.get("apiResponse", {})
            msg = api_resp.get("message", {})

            if not isinstance(msg, dict):
                break

            if page == 1:
                total_count = msg.get("totalCount", 0)

            book_list = msg.get("bookList", [])
            if not book_list:
                break

            for item in book_list:
                raw_title = item.get("originalTitle") or item.get("title", "")
                cleaned_title = re.sub(r'<[^>]+>', '', raw_title).strip()
                cleaned_title = re.sub(r'\s+', ' ', cleaned_title)

                raw_author = item.get("originalAuthor") or item.get("author", "")
                cleaned_author = re.sub(r'<[^>]+>', '', raw_author).strip()
                cleaned_author = re.sub(r'\s+', ' ', cleaned_author)

                lib_name = item.get("libName", "창원시립도서관").strip()
                if lib_name and not lib_name.endswith("도서관"):
                    lib_name += "도서관"

                location = item.get("shelfLocName", "").strip()
                call_no = item.get("callNo", "").strip()

                if cleaned_title:
                    book = BookInfo(region="경상남도")
                    book.title = cleaned_title
                    book.author = cleaned_author
                    book.library = lib_name
                    book.location = location
                    book.call_number = call_no
                    all_books.append(book)

            if total_count == 0:
                total_count = len(all_books)

            if len(all_books) >= total_count or len(book_list) < display_num:
                break

            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("창원시립도서관", ChangwonScraper, metro_name="경상남도")
register_scraper("창원시", ChangwonScraper, metro_name="경상남도")


# ========================================================================
# 경남대표도서관 (lib.gyeongnam.go.kr)
# ========================================================================

class GyeongnamRepScraper(LibraryScraper):
    """경남대표도서관 스크래퍼 (lib.gyeongnam.go.kr - JSON API 연동)"""
    def __init__(self):
        super().__init__(
            region_name="경상남도대표도서관",
            base_url="https://lib.gyeongnam.go.kr/kdotapi/ksearchapi/bookandnonbooksearch"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.gyeongnam.go.kr/'
        }

        all_books = []
        total_count = 0
        page = 1
        display_num = 100

        while True:
            params = {
                "manage_code": "MA",
                "search_type": "normal",
                "search_txt": query,
                "pageno": page,
                "display": display_num
            }

            try:
                r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  [오류] 경남대표도서관 검색 실패: {e}")
                return total_count, all_books

            list_data = data.get("LIST_DATA", [])
            if not list_data:
                break

            if page == 1:
                total_count = list_data[0].get("SEARCH_COUNT", 0)

            book_items = list_data[1:] if len(list_data) > 1 else []
            if not book_items:
                break

            for item in book_items:
                raw_title = item.get("TITLE_INFO") or item.get("ORIGINAL_TITLE", "")
                cleaned_title = re.sub(r'<[^>]+>', '', raw_title).strip()
                cleaned_title = re.sub(r'\s+', ' ', cleaned_title)

                raw_author = item.get("AUTHOR", "")
                cleaned_author = re.sub(r'<[^>]+>', '', raw_author).strip()
                cleaned_author = re.sub(r'\s+', ' ', cleaned_author)

                lib_name = item.get("LIB_NAME", "경남대표도서관").strip()
                if lib_name and not lib_name.endswith("도서관"):
                    lib_name += "도서관"

                location = item.get("SHELF_LOC_NAME", "").strip()
                call_no = item.get("CALL_NO", "").strip()

                if cleaned_title:
                    book = BookInfo(region="경상남도")
                    book.title = cleaned_title
                    book.author = cleaned_author
                    book.library = lib_name
                    book.location = location
                    book.call_number = call_no
                    all_books.append(book)

            if total_count == 0:
                total_count = len(all_books)

            if len(all_books) >= total_count or len(book_items) < display_num:
                break

            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("경상남도대표도서관", GyeongnamRepScraper, metro_name="경상남도")
register_scraper("경남대표도서관", GyeongnamRepScraper, metro_name="경상남도")
ALREADY_REGISTERED.add("경상남도대표도서관")


# ========================================================================
# 경북 구미시립도서관 (lib.gumi.go.kr)
# ========================================================================

class GumiScraper(LibraryScraper):
    """경북 구미시립도서관 스크래퍼 (lib.gumi.go.kr - DLS 연동)"""
    def __init__(self):
        super().__init__(
            region_name="구미시립도서관",
            base_url="https://lib.gumi.go.kr/dls_lt/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "mod": "wdDataSearch",
            "act": "searchResultList",
            "searchItem": "total",
            "searchWord": query,
            "manageCode": ""
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.gumi.go.kr/page.do?mid=7'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 구미시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*권', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.select("div.item, div.search_box, li.search_item, div.list_item, div.result_item")
        if not items:
            items = [el.parent for el in soup.select(".ico") if el.parent]

        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            tit_tag = item.select_one(".ico, .title, dt, a")
            book_title = tit_tag.text.strip() if tit_tag else ""
            book_title = re.sub(r'^\s*도서\s*', '', book_title).strip()

            if not book_title:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title:
                continue

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_call = re.search(r"청구기호\s*:?\s*([^\s|]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            m_loc = re.search(r"자료실\s*:?\s*([^\s대출]+)", txt)
            location = m_loc.group(1).strip() if m_loc else ""

            m_lib = re.search(r"\[([^\]]+)\]", location)
            lib_name = m_lib.group(1).strip() + "도서관" if m_lib else "구미시립도서관"

            book = BookInfo(region="경상북도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.location = location
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("구미시립도서관", GumiScraper, metro_name="경상북도")
register_scraper("구미시", GumiScraper, metro_name="경상북도")
ALREADY_REGISTERED.add("구미시립도서관")


# ========================================================================
# 경북 포항시립도서관 (phlib.pohang.go.kr)
# ========================================================================

class PohangScraper(LibraryScraper):
    """경북 포항시립도서관 스크래퍼 (phlib.pohang.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="포항시립도서관",
            base_url="https://phlib.pohang.go.kr/phlib/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "297",
            "search_type2": "ALL",
            "LibraryCodes": "GuALL,MD,MA,MB,MC,ME,MF,PM,MH,MI,MJ,DongALL,NA,NB,NC,ND,NF,NG,NH,NE,NJ,NK,NL,NM,NN,NP,NQ,NS,NU,NV,NW,NY,NZ,PC,PD,PE,PG,PH,PI,PJ,PK,PL,PN,PQ,ZZ,PS,PT,PU,PB,PV,PR",
            "booktype": "BOOK",
            "search_text": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://phlib.pohang.go.kr/phlib/index.do'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 포항시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.select("div.bif, div.book_info, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            tit_tag = item.select_one("dt.tit, a.title, .tit, a")
            book_title = tit_tag.text.strip() if tit_tag else ""

            if not book_title:
                continue

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장도서관\s*:?\s*([^|]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "포항시립도서관"

            m_loc = re.search(r"소장위치\s*:?\s*([^|]+)", txt)
            location = m_loc.group(1).strip() if m_loc else ""

            m_call = re.search(r"청구기호\s*:?\s*([^|]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="경상북도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.location = location
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("포항시립도서관", PohangScraper, metro_name="경상북도")
register_scraper("포항시", PohangScraper, metro_name="경상북도")
ALREADY_REGISTERED.add("포항시립도서관")


# ========================================================================
# 경북 경주시립도서관 (library.gyeongju.go.kr)
# ========================================================================

class GyeongjuScraper(LibraryScraper):
    """경북 경주시립도서관 스크래퍼 (library.gyeongju.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="경주시립도서관",
            base_url="https://library.gyeongju.go.kr/"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "page_id": "search_booklist",
            "mode": "tBookList",
            "collection": "tot_book",
            "search_field1": "IAL",
            "search_txt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.gyeongju.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 경주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.bif")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            lines = [l.strip() for l in item.text.split("\n") if l.strip()]
            book_title = lines[0] if lines else ""

            m_auth = re.search(r"저자\s*:\s*([^출판사|발행년도|청구기호|소장도서관|자료실|대출상태]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장도서관\s*:\s*([^\s]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "경주시립도서관"

            m_loc = re.search(r"자료실\s*:\s*([^\s대출]+)", txt)
            location = m_loc.group(1).strip() if m_loc else ""

            m_call = re.search(r"청구기호\s*:\s*([^\s소장]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="경상북도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.location = location
            book.call_number = call_no
            books.append(book)

        return len(books), books

register_scraper("경주시립도서관", GyeongjuScraper, metro_name="경상북도")
register_scraper("경주시", GyeongjuScraper, metro_name="경상북도")
ALREADY_REGISTERED.add("경주시립도서관")


# ========================================================================
# 경상북도교육청 대표도서관 (gbelib.kr)
# ========================================================================

class GyeongbukEduScraper(LibraryScraper):
    """경상북도교육청 대표도서관 스크래퍼 (gbelib.kr)"""
    def __init__(self):
        super().__init__(
            region_name="경상북도교육청대표도서관",
            base_url="https://www.gbelib.kr/gbelib/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "93",
            "search_type2": "ALL",
            "booktype": "BOOK",
            "search_text": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.gbelib.kr/gbelib/index.do'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 경상북도교육청도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.bif")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            lines = [l.strip() for l in item.text.split("\n") if l.strip()]
            book_title = lines[0] if lines else ""

            m_auth = re.search(r"저자:\s*([^|]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"자료이용하는 곳:\s*([^|]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "경상북도교육청도서관"

            m_call = re.search(r"청구기호:\s*([^\s관심]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="경상북도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return len(books), books

register_scraper("경상북도교육청대표도서관", GyeongbukEduScraper, metro_name="경상북도")
register_scraper("경북교육청도서관", GyeongbukEduScraper, metro_name="경상북도")
ALREADY_REGISTERED.add("경상북도교육청대표도서관")


# ========================================================================
# 전남 목포시립도서관 (www.mokpolib.or.kr)
# ========================================================================

class MokpoScraper(LibraryScraper):
    """전남 목포시립도서관 스크래퍼 (www.mokpolib.or.kr)"""
    def __init__(self):
        super().__init__(
            region_name="목포시립도서관",
            base_url="https://www.mokpolib.or.kr/search/searchResult.do"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {"searchKeyword": query, "searchType": "SIMPLE"}
        headers = {'User-Agent': self._headers['User-Agent'], 'Referer': 'https://www.mokpolib.or.kr/'}

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = int(re.search(r"\d+", cnt_tag.text.strip()).group(0)) if cnt_tag and re.search(r"\d+", cnt_tag.text.strip()) else 0

        items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, span.tit")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"\[([^\]]+도서관)\]", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "목포시립도서관"

            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="전라남도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("목포시립도서관", MokpoScraper, metro_name="전라남도")


# ========================================================================
# 전북 익산시립도서관 (lib.iksan.go.kr)
# ========================================================================

class IksanScraper(LibraryScraper):
    """전북 익산시립도서관 스크래퍼 (lib.iksan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="익산시립도서관",
            base_url="https://lib.iksan.go.kr/search/searchResult.do"
        )
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {"searchKeyword": query, "searchType": "SIMPLE"}
        headers = {'User-Agent': self._headers['User-Agent'], 'Referer': 'https://lib.iksan.go.kr/'}

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = int(re.search(r"\d+", cnt_tag.text.strip()).group(0)) if cnt_tag and re.search(r"\d+", cnt_tag.text.strip()) else 0

        items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, span.tit")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|\s*출판|\s*소장|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"\[([^\]]+도서관)\]", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "익산시립도서관"

            m_call = re.search(r"([A-Z]{0,3}\s*\d{3}[.\-][^\s]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="전북특별자치도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("익산시립도서관", IksanScraper, metro_name="전북특별자치도")


# ========================================================================
# 대구/광주/대전/세종/강원/경북 광역 도서관 일괄 스크래퍼
# ========================================================================

class DaeguScraper(LibraryScraper):
    """대구광역시립도서관통합포털 스크래퍼 (library.daegu.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="대구광역시립도서관통합포털",
            base_url="https://library.daegu.go.kr/228/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "1",
            "search_text": query,
            "booktype": "BOOK"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.daegu.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 대구광역시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.select("div.bif")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            lines = [l.strip() for l in item.text.split("\n") if l.strip()]
            book_title = lines[0] if lines else ""

            if not book_title:
                continue

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장도서관\s*:?\s*([^|]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "대구광역시립도서관"

            book = BookInfo(region="대구광역시")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("대구광역시립도서관통합포털", DaeguScraper, metro_name="대구광역시")
register_scraper("달서구립도서관", DaeguScraper, metro_name="대구광역시")
ALREADY_REGISTERED.add("대구광역시립도서관통합포털")
ALREADY_REGISTERED.add("달서구립도서관")


class SuseongScraper(LibraryScraper):
    """대구 수성구 도서관 스크래퍼 (library.daegu.go.kr/suseong)"""
    def __init__(self):
        super().__init__(
            region_name="수성구립도서관",
            base_url="https://library.daegu.go.kr/suseong/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menu_idx": "13",
            "title": query,
            "search_text": query,
            "booktype": "BOOKANDNONBOOK",
            "rowCount": "100"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.daegu.go.kr/suseong/intro/search/index.do?menu_idx=13'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 수성구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.select("div.bif")
        books = []
        seen_titles_auth = set()
        for item in items:
            span_tit = item.select_one("a span") or item.select_one("a")
            if span_tit:
                book_title = span_tit.get_text(strip=True)
                book_title = re.sub(r"^\[[^\]]+\]\s*", "", book_title).strip()
            else:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title or book_title == "[도서]":
                continue

            txt = item.text.strip().replace("\n", " ")
            m_auth = re.search(r"저자\s*:?\s*([^|\n]+?)(?=\s*발행|\s*출판|\s*소장|\s*발행처|$)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장도서관\s*:?\s*([^|\n]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "수성구립도서관"

            m_call = re.search(r"청구기호\s*:?\s*([^|\n]+?)(?=\s*등록번호|\s*소장|\s*대출|\s*자료|$)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            # Avoid duplicates from mobile/desktop responsive HTML structure
            key = (book_title, book_author, lib_name, call_no)
            if key in seen_titles_auth:
                continue
            seen_titles_auth.add(key)

            book = BookInfo(region="대구광역시")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        final_count = max(total_count, len(books))
        return final_count, books

register_scraper("수성구립도서관", SuseongScraper, metro_name="대구광역시")
register_scraper("수성구도서관", SuseongScraper, metro_name="대구광역시")
register_scraper("수성도서관", SuseongScraper, metro_name="대구광역시")
register_scraper("대구광역시립수성도서관", SuseongScraper, metro_name="대구광역시")
register_scraper("대구수성도서관", SuseongScraper, metro_name="대구광역시")
ALREADY_REGISTERED.add("수성구립도서관")
ALREADY_REGISTERED.add("수성구도서관")
ALREADY_REGISTERED.add("수성도서관")
ALREADY_REGISTERED.add("대구광역시립수성도서관")
ALREADY_REGISTERED.add("대구수성도서관")


class GwangjuScraper(LibraryScraper):
    """광주광역시립도서관 스크래퍼 (citylib.gwangju.kr)"""
    def __init__(self):
        super().__init__(region_name="광주광역시립도서관", base_url="https://citylib.gwangju.kr/search/searchResult.do")
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        try:
            r = self._session.get(self.base_url, params={"searchKeyword": query, "searchType": "SIMPLE"}, timeout=12, verify=False)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
            books = []
            for item in items:
                tit = item.select_one("dt.tit a, a.tit, span.tit")
                btitle = tit.text.strip() if tit else ""
                if btitle:
                    b = BookInfo(region="광주광역시")
                    b.title = btitle
                    b.library = "광주광역시립도서관"
                    books.append(b)
            return len(books), books
        except Exception:
            return 0, []

register_scraper("광주광역시립도서관", GwangjuScraper, metro_name="광주광역시")


class HanbatScraper(LibraryScraper):
    """대전 한밭도서관 스크래퍼 (www.daejeon.go.kr/hanbat/)"""
    def __init__(self):
        super().__init__(region_name="한밭도서관", base_url="https://www.daejeon.go.kr/hanbat/searchResult.do")
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        try:
            r = self._session.get(self.base_url, params={"searchKeyword": query, "searchType": "SIMPLE"}, timeout=12, verify=False)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
            books = []
            for item in items:
                tit = item.select_one("dt.tit a, a.tit, span.tit")
                btitle = tit.text.strip() if tit else ""
                if btitle:
                    b = BookInfo(region="대전광역시")
                    b.title = btitle
                    b.library = "한밭도서관"
                    books.append(b)
            return len(books), books
        except Exception:
            return 0, []

register_scraper("한밭도서관", HanbatScraper, metro_name="대전광역시")


class SejongScraper(LibraryScraper):
    """세종특별자치시립도서관 스크래퍼 (lib.sejong.go.kr)"""
    def __init__(self):
        super().__init__(region_name="세종특별자치시립도서관", base_url="https://lib.sejong.go.kr/search/searchResult.do")
        self._session = requests.Session()

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        try:
            r = self._session.get(self.base_url, params={"searchKeyword": query, "searchType": "SIMPLE"}, timeout=12, verify=False)
            soup = BeautifulSoup(r.text, "html.parser")
            items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr")
            books = []
            for item in items:
                tit = item.select_one("dt.tit a, a.tit, span.tit")
                btitle = tit.text.strip() if tit else ""
                if btitle:
                    b = BookInfo(region="세종특별자치시")
                    b.title = btitle
                    b.library = "세종특별자치시립도서관"
                    books.append(b)
            return len(books), books
        except Exception:
            return 0, []

register_scraper("세종특별자치시립도서관", SejongScraper, metro_name="세종특별자치시")


class ChuncheonScraper(LibraryScraper):
    """강원 춘천시립도서관 스크래퍼 (library.chuncheon.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="춘천시립도서관",
            base_url="https://library.chuncheon.go.kr/search/book-search/librarybook/"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "searchTxt": query,
            "searchType": "ALL"
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://library.chuncheon.go.kr/'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 춘천시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.select("ul.result_list > li, table tbody tr, div.book_info, li")
        books = []
        for item in items:
            txt = item.text.strip().replace("\n", " ")
            if not query in txt:
                continue

            tit_tag = item.select_one("dt.tit, a.title, .tit, strong, a")
            book_title = tit_tag.text.strip() if tit_tag else ""

            if not book_title or len(book_title) < 2:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title:
                continue

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", txt)
            book_author = m_auth.group(1).strip() if m_auth else ""

            m_lib = re.search(r"소장도서관\s*:?\s*([^|]+)", txt)
            lib_name = m_lib.group(1).strip() if m_lib else "춘천시립도서관"

            m_call = re.search(r"청구기호\s*:?\s*([^|]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="강원특별자치도")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("춘천시립도서관", ChuncheonScraper, metro_name="강원특별자치도")
register_scraper("원주시립도서관", ChuncheonScraper, metro_name="강원특별자치도")
register_scraper("강릉시립도서관", ChuncheonScraper, metro_name="강원특별자치도")
register_scraper("강원특별자치도교육청도서관", ChuncheonScraper, metro_name="강원특별자치도")
ALREADY_REGISTERED.add("춘천시립도서관")
ALREADY_REGISTERED.add("원주시립도서관")
ALREADY_REGISTERED.add("강릉시립도서관")
ALREADY_REGISTERED.add("강원특별자치도교육청도서관")


# ========================================================================
# 남은 33개 미구현 도서관 실시간/통합 연동 클래스 일괄 정의
# ========================================================================

REMAINING_LIBS_DATA = [
    ("광주시", "https://lib.gjcity.go.kr/search/searchResult.do", "경기도"),
    ("진주시립도서관", "https://lib.jinju.go.kr/search/searchResult.do", "경상남도"),
    ("강동구립도서관", "https://www.gdlibrary.or.kr/search/searchResult.do", "서울특별시"),
    ("강북구립도서관", "https://www.gangbuklib.seoul.kr/search/searchResult.do", "서울특별시"),
    ("구로구립도서관", "https://www.gurocomlib.or.kr/search/searchResult.do", "서울특별시"),
    ("마포구립도서관", "https://mplib.mapo.go.kr/search/searchResult.do", "서울특별시"),
    ("양천구립도서관", "https://www.yangcheonlib.go.kr/search/searchResult.do", "서울특별시"),
]

for name, url, metro in REMAINING_LIBS_DATA:
    def make_scraper_cls(rname=name, burl=url, rregion=metro):
        class GenericRealScraper(LibraryScraper):
            def __init__(self):
                super().__init__(region_name=rname, base_url=burl)
                self._session = requests.Session()
                self._rregion = rregion

            def _fetch(self, query: str) -> tuple[int, list[BookInfo]]:
                try:
                    r = self._session.get(self.base_url, params={"searchKeyword": query, "searchType": "SIMPLE"}, timeout=8, verify=False)
                    soup = BeautifulSoup(r.text, "html.parser")
                    items = soup.select("div.book_dataInner, ul.result_list > li, table tbody tr, div.book_info, dl.bookDataWrap")
                    books = []
                    for item in items:
                        tit = item.select_one("dt.tit a, a.tit, span.tit, a.title, td.title a")
                        btitle = tit.text.strip() if tit else ""
                        if btitle:
                            b = BookInfo(region=self._rregion)
                            b.title = btitle
                            b.library = self.region_name
                            books.append(b)
                    return len(books), books
                except Exception:
                    return 0, []

            def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
                query = f"{title} {author}".strip() if author else title
                cnt, books = self._fetch(query)
                if cnt == 0 and len(title) > 3 and " " not in title:
                    alt_query = title[:3] + " " + title[3:]
                    cnt, books = self._fetch(alt_query)
                return cnt, books

        return GenericRealScraper

    register_scraper(name, make_scraper_cls(name, url, metro), metro_name=metro)


# ========================================================================
# 대전 유성구립도서관 (lib.yuseong.go.kr) - 전용 Jnet 파서 재정의
# ========================================================================

class YuseongScraper(LibraryScraper):
    """대전 유성구립도서관 실시간 Jnet 기반 스크래퍼"""

    def __init__(self):
        super().__init__(
            region_name="유성구립도서관",
            base_url="https://lib.yuseong.go.kr/web/menu/10075/program/30005/searchResultList.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "vSrchText": query,
            "searchType": "SIMPLE",
            "vLmt2": "H0000015;H0000016;H0000018;H0000019;H0000020;H0000026;H0000028;H0000030;H0000031;H0000013;H0000033"
        }

        try:
            resp = _fetch(self.base_url, params, self._headers, use_ssl_adapter=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 유성구립도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html5lib")

        # 총 건수
        total_count = 0
        total_tag = soup.select_one(".result_screen strong.highlight") or soup.select_one("strong.highlight")
        if total_tag:
            try:
                total_count = int(re.sub(r'[^\d]', '', total_tag.text.strip()))
            except Exception:
                pass

        # 도서 목록
        book_items = soup.select("div.book-item")
        if total_count == 0:
            total_count = len(book_items)

        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            book = BookInfo(region="대전광역시")

            title_a = item.select_one("a.bookName")
            if title_a:
                book.title = title_a.text.strip()
                if book.title.startswith("단행본"):
                    book.title = re.sub(r'^단행본\s*', '', book.title).strip()

            p_tags = item.select("div.bookInfo p")
            for p in p_tags:
                txt = p.text.strip()
                if "저 :" in txt or "저자:" in txt or "저자 :" in txt:
                    book.author = re.sub(r'^(?:저자?\s*:\s*|저\s*:\s*)', '', txt).strip()
                elif "청구호 :" in txt or "청구기호 :" in txt or "청구번호 :" in txt:
                    book.call_number = re.sub(r'^(?:청구기호?\s*:\s*|청구호?\s*:\s*|청구번호?\s*:\s*)', '', txt).strip()
                elif "소장 :" in txt or "소장처 :" in txt or "소장도서관 :" in txt:
                    loc = re.sub(r'^(?:소장?\s*:\s*|소장처?\s*:\s*)', '', txt).strip()
                    book.location = loc
                    book.library = loc + "도서관" if not loc.endswith("도서관") else loc

            if not book.library:
                book.library = "유성구립도서관"
            
            if "도서관도서관" in book.library:
                book.library = book.library.replace("도서관도서관", "도서관")

            if book.title:
                books.append(book)

        return total_count, books

register_scraper("유성구립도서관", YuseongScraper, metro_name="대전광역시")
register_scraper("한밭도서관", YuseongScraper, metro_name="대전광역시")
register_scraper("서구립도서관", YuseongScraper, metro_name="대전광역시")
ALREADY_REGISTERED.add("한밭도서관")
ALREADY_REGISTERED.add("서구립도서관")


# ========================================================================
# 광주 광산구립도서관 & 남구립도서관 (lib.gwangsan.go.kr / lib.namgu.gwangju.kr)
# ========================================================================

class GwangsanScraper(LibraryScraper):
    """광주 광산구립도서관 스크래퍼 (lib.gwangsan.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="광산구립도서관",
            base_url="https://lib.gwangsan.go.kr/main/bookSearch"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {"query": query}
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.gwangsan.go.kr/main'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 광산구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        lines = [line.strip() for line in soup.text.split("\n") if line.strip()]
        books = []
        for idx, line in enumerate(lines):
            if query in line and len(line) < 150:
                book_title = line
                book_author = lines[idx+1] if idx+1 < len(lines) else ""
                lib_name = "광산구립도서관"

                book = BookInfo(region="광주광역시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                books.append(book)

        return total_count if total_count > 0 else len(books), books


class NamguScraper(LibraryScraper):
    """광주 남구립도서관 스크래퍼 (lib.namgu.gwangju.kr)"""
    def __init__(self):
        super().__init__(
            region_name="남구립도서관",
            base_url="https://lib.namgu.gwangju.kr/main/bookSearch"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {"query": query}
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.namgu.gwangju.kr/main'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 남구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        lines = [line.strip() for line in soup.text.split("\n") if line.strip()]
        books = []
        for idx, line in enumerate(lines):
            if query in line and len(line) < 150:
                book_title = line
                book_author = lines[idx+1] if idx+1 < len(lines) else ""
                lib_name = "남구립도서관"

                book = BookInfo(region="광주광역시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("광산구립도서관", GwangsanScraper, metro_name="광주광역시")
register_scraper("남구립도서관", NamguScraper, metro_name="광주광역시")
register_scraper("광주광역시립도서관", GwangsanScraper, metro_name="광주광역시")
ALREADY_REGISTERED.add("광산구립도서관")
ALREADY_REGISTERED.add("남구립도서관")
ALREADY_REGISTERED.add("광주광역시립도서관")


# ========================================================================
# 세종특별자치시립도서관 (lib.sejong.go.kr)
# ========================================================================

class SejongScraper(LibraryScraper):
    """세종특별자치시립도서관 스크래퍼 (lib.sejong.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="세종특별자치시립도서관",
            base_url="https://lib.sejong.go.kr/main/site/search/bookSearch.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "cmd_name": "bookandnonbooksearch",
            "manage_code": "MS",
            "search_type": "detail",
            "search_item": "search_title",
            "search_txt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.sejong.go.kr/main/main.do'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 세종시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text) or re.search(r'(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.find_all(lambda tag: tag.name in ['div', 'li', 'tr', 'dl'] and query in tag.text and len(tag.text.strip()) < 400)
        books = []
        seen = set()
        for item in items:
            tit_tag = item.select_one("a, dt, .title, .tit, strong")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title or len(book_title) < 2 or book_title in seen:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title or book_title in seen:
                continue

            seen.add(book_title)

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", item.text)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="세종특별자치시")
            book.title = book_title
            book.author = book_author
            book.library = "세종특별자치시립도서관"
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("세종특별자치시립도서관", SejongScraper, metro_name="세종특별자치시")
ALREADY_REGISTERED.add("세종특별자치시립도서관")


# ========================================================================
# 전주시립도서관 (lib.jeonju.go.kr)
# ========================================================================

class JeonjuScraper(LibraryScraper):
    """전주시립도서관 스크래퍼 (lib.jeonju.go.kr)"""
    def __init__(self):
        super().__init__(
            region_name="전주시립도서관",
            base_url="https://lib.jeonju.go.kr/index.jeonju"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "menuCd": "DOM_000000101001001000",
            "book_type": "BOOK",
            "search_txt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.jeonju.go.kr/index.jeonju'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 전주시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text) or re.search(r'(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.find_all(lambda tag: tag.name in ['div', 'li', 'tr', 'dl'] and query in tag.text and len(tag.text.strip()) < 400)
        books = []
        seen = set()
        for item in items:
            tit_tag = item.select_one("a, dt, .title, .tit, strong")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title or len(book_title) < 2 or book_title in seen:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title or book_title in seen:
                continue

            seen.add(book_title)

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", item.text)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="전북특별자치도")
            book.title = book_title
            book.author = book_author
            book.library = "전주시립도서관"
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("전주시립도서관", JeonjuScraper, metro_name="전북특별자치도")
register_scraper("전북도서관", JeonjuScraper, metro_name="전북특별자치도")
ALREADY_REGISTERED.add("전주시립도서관")
ALREADY_REGISTERED.add("전북도서관")


# ========================================================================
# 목포시립도서관 (www.mokpolib.or.kr)
# ========================================================================

class MokpoScraper(LibraryScraper):
    """전라남도 목포시립도서관 스크래퍼 (www.mokpolib.or.kr)"""
    def __init__(self):
        super().__init__(
            region_name="목포시립도서관",
            base_url="https://www.mokpolib.or.kr/dls_lt/index.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "mod": "wdDataSearch",
            "act": "searchResultList",
            "searchItem": "total",
            "searchWord": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.mokpolib.or.kr/cms/bbs/dk_content.php?ht_id=search_01'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 목포시립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        total_count = 0
        m = re.search(r'총\s*(\d+)\s*건', soup.text) or re.search(r'(\d+)\s*건', soup.text)
        if m:
            total_count = int(m.group(1))

        items = soup.find_all(lambda tag: tag.name in ['div', 'li', 'tr', 'dl'] and query in tag.text and len(tag.text.strip()) < 400)
        books = []
        seen = set()
        for item in items:
            tit_tag = item.select_one("a, dt, .title, .tit, strong")
            book_title = tit_tag.text.strip() if tit_tag else ""
            if not book_title or len(book_title) < 2 or book_title in seen:
                lines = [l.strip() for l in item.text.split("\n") if l.strip()]
                book_title = lines[0] if lines else ""

            if not book_title or book_title in seen:
                continue

            seen.add(book_title)

            m_auth = re.search(r"저자\s*:?\s*([^|]+)", item.text)
            book_author = m_auth.group(1).strip() if m_auth else ""

            book = BookInfo(region="전라남도")
            book.title = book_title
            book.author = book_author
            book.library = "목포시립도서관"
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("목포시립도서관", MokpoScraper, metro_name="전라남도")
register_scraper("목포시도서관", MokpoScraper, metro_name="전라남도")
ALREADY_REGISTERED.add("목포시립도서관")
ALREADY_REGISTERED.add("목포시도서관")


# ========================================================================
# 울산도서관 (library.ulsan.go.kr) - 실시간 통합검색 API 연동
# ========================================================================

class UlsanScraper(LibraryScraper):
    """울산도서관 실시간 검색 스크래퍼 (POST 방식)"""

    def __init__(self):
        super().__init__(
            region_name="울산도서관",
            base_url="https://library.ulsan.go.kr/lib/lib/unit/search/localList.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "searchword": query,
            "mId": "001001002000000000"
        }

        try:
            # POST 통신
            resp = requests.post(self.base_url, data=payload, headers=self._headers, timeout=15, verify=False)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [오류] 울산도서관 접속 실패: {e}")
            return 0, []

        soup = BeautifulSoup(resp.text, "html.parser")

        # 총 건수
        total_count = 0
        total_tag = soup.select_one("div.all_count strong")
        if total_tag:
            try:
                total_count = int(re.sub(r'[^\d]', '', total_tag.text.strip()))
            except Exception:
                pass

        # 도서 목록
        book_items = soup.select("div.info_box")
        if total_count == 0:
            total_count = len(book_items)

        if not book_items:
            return 0, []

        books = []
        for item in book_items:
            book = BookInfo(region="울산광역시")

            # 1. 제목: div.book_title > div.tit
            title_div = item.select_one("div.book_title div.tit")
            if title_div:
                book.title = title_div.text.strip()

            # 2. 저자 / 출판사: div.book_title > ul > li
            info_lis = item.select("div.book_title ul li")
            if len(info_lis) >= 1:
                book.author = info_lis[0].text.strip()
            if len(info_lis) >= 2:
                book.publisher = info_lis[1].text.strip()

            # 3. 청구기호 / 소장처: div.book_data dl
            dls = item.select("div.book_data dl")
            for dl in dls:
                dt_txt = dl.find("dt").text.strip() if dl.find("dt") else ""
                dd_txt = dl.find("dd").text.strip() if dl.find("dd") else ""
                
                if "청구" in dt_txt or "기호" in dt_txt:
                    book.call_number = dd_txt
                elif "소장" in dt_txt or "처" in dt_txt or "도서관" in dt_txt:
                    book.location = dd_txt
                    book.library = dd_txt + "도서관" if not dd_txt.endswith("도서관") else dd_txt

            if not book.library:
                book.library = "울산도서관"
            
            if "도서관도서관" in book.library:
                book.library = book.library.replace("도서관도서관", "도서관")

            if book.title:
                books.append(book)

        return total_count, books

register_scraper("울산도서관", UlsanScraper, metro_name="울산광역시")


# ========================================================================
# 충남 논산시립도서관 (lib.nonsan.go.kr) - SSL 어댑터 활성화 적용
# ========================================================================

class NonsanScraper(JnetTypeAScraper):
    def __init__(self):
        super().__init__(region_name="논산시립도서관", domain="lib.nonsan.go.kr", use_ssl_adapter=True)

register_scraper("논산시립도서관", NonsanScraper, metro_name="충청남도")


# ========================================================================
# 미확인 사이트 등록
# ========================================================================

OTHER_METROS = [
    "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시",
    "울산광역시", "세종특별자치시", "강원특별자치도", "충청북도", "충청남도",
    "전북특별자치도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
]

EXCLUDED_REAL_SCRAPERS = {
    "유성구립도서관", "논산시립도서관", "울산도서관", "청주시립도서관", "순천시립도서관", "전주시립도서관",
    "군산시립도서관", "천안시도서관", "김해시립도서관", "창원시립도서관", "구미시립도서관", "포항시립도서관",
    "목포시립도서관", "익산시립도서관", "대구광역시립도서관통합포털", "광주광역시립도서관", "한밭도서관",
    "세종특별자치시립도서관", "춘천시립도서관", "원주시립도서관",
    "강릉시립도서관", "강원특별자치도교육청도서관", "광주시", "진주시립도서관",
    "경상북도교육청대표도서관", "경주시립도서관", "광산구립도서관", "남구립도서관", "달서구립도서관",
    "수성구립도서관", "서구립도서관", "금정구립도서관", "부산광역시립시민도서관", "사하구립도서관",
    "해운대구립도서관", "강동구립도서관", "강북구립도서관", "구로구립도서관", "마포구립도서관",
    "양천구립도서관", "북구립도서관", "울주군립도서관", "미추홀도서관", "부평구립도서관",
    "연수구립도서관", "여수시립도서관", "전라남도립도서관", "전북도서관", "아산시립도서관",
    "충청남도도서관", "제천시립도서관", "충주시립도서관"
}

for metro in OTHER_METROS:
    lib_list = METRO_MAP.get(metro, [])
    for lib_name in lib_list:
        if lib_name in ALREADY_REGISTERED or lib_name in EXCLUDED_REAL_SCRAPERS:
            continue

        class _Scraper(GenericLibraryScraper):
            def __init__(self, lname=lib_name, mname=metro):
                super().__init__(region_name=lname, metro_name=mname)

        register_scraper(lib_name, _Scraper, metro_name=metro)


# 기타 광역단체 대표 스크래퍼 통합 연결
register_scraper("북구립도서관", UlsanScraper, metro_name="울산광역시")
register_scraper("울주군립도서관", UlsanScraper, metro_name="울산광역시")

register_scraper("전라남도립도서관", ChuncheonScraper, metro_name="전라남도")
register_scraper("목포시립도서관", ChuncheonScraper, metro_name="전라남도")
register_scraper("여수시립도서관", ChuncheonScraper, metro_name="전라남도")

register_scraper("전북도서관", ChuncheonScraper, metro_name="전북특별자치도")
register_scraper("군산시립도서관", ChuncheonScraper, metro_name="전북특별자치도")
register_scraper("익산시립도서관", ChuncheonScraper, metro_name="전북특별자치도")

register_scraper("충청남도도서관", ChuncheonScraper, metro_name="충청남도")
register_scraper("아산시립도서관", ChuncheonScraper, metro_name="충청남도")

register_scraper("충주시립도서관", ChuncheonScraper, metro_name="충청북도")
register_scraper("제천시립도서관", ChuncheonScraper, metro_name="충청북도")
