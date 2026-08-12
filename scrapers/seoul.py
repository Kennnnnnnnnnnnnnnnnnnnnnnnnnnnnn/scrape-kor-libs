"""
서울특별시 도서관 스크래퍼 모듈
- jnet 엔드포인트가 확인된 도서관: 실제 스크래퍼 등록
- 서울도서관(대표): LISOS 기반 전용 스크래퍼 등록
- 성북구립도서관: LISOS 기반 전용 스크래퍼 등록
- 미확인 도서관: GenericLibraryScraper (빈 결과 반환)
"""
from .registry import register_scraper
from .jnet import JnetTypeAScraper, JnetTypeBScraper
from .seoullib import SeoulLibScraper
from .seongbuklib import SeongbukScraper
from .generic import GenericLibraryScraper
from .base import BookInfo, LibraryScraper
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter
import re
import requests
from bs4 import BeautifulSoup

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'

class _SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


# ========================================================================
# 서울도서관(대표) - LISOS 전용 스크래퍼
# ========================================================================
register_scraper("서울도서관", SeoulLibScraper, metro_name="서울특별시")


# ========================================================================
# 성북구립도서관 - 전용 스크래퍼
# ========================================================================
register_scraper("성북구립도서관", SeongbukScraper, metro_name="서울특별시")


# ========================================================================
# jnet Type A 확인된 사이트
# ========================================================================

# 서울시교육청도서관 (lib.sen.go.kr)
class SeoulEducationScraper(JnetTypeAScraper):
    def __init__(self):
        super().__init__(region_name="서울시교육청도서관", domain="lib.sen.go.kr")

register_scraper("서울시교육청도서관", SeoulEducationScraper, metro_name="서울특별시")


# ========================================================================
# jnet Type B 확인된 사이트
# ========================================================================

# 강남구립도서관
class GangnamScraper(JnetTypeBScraper):
    def __init__(self):
        super().__init__(region_name="강남구립도서관", domain="library.gangnam.go.kr")

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        total_count, all_books = super().search(title, author)
        for b in all_books:
            if b.library.startswith("강남구립도서관 "):
                b.library = b.library.replace("강남구립도서관 ", "")
            if not b.library.endswith("도서관"):
                b.library += "도서관"
            if "도서관도서관" in b.library:
                b.library = b.library.replace("도서관도서관", "도서관")
        return total_count, all_books

register_scraper("강남구립도서관", GangnamScraper, metro_name="서울특별시")


# 송파구립도서관
class SongpaScraper(LibraryScraper):
    """송파구립도서관 전용 실시간 검색 스크래퍼"""

    def __init__(self):
        super().__init__(
            region_name="송파구립도서관",
            base_url="https://www.splib.or.kr/intro/program/plusSearchResultList.do"
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        from .jnet import _fetch
        all_books = []
        total_count = 0
        page = 1

        while True:
            params = {
                "searchKeyword": query,
                "searchType": "SIMPLE",
                "searchCategory": "BOOK",
                "searchKey": "ALL",
                "searchLibrary": "ALL",
                "searchDisplay": "100",
                "currentPageNo": str(page)
            }

            try:
                resp = _fetch(self.base_url, params, self._headers, use_ssl_adapter=False)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"  [오류] 송파구립도서관 접속 실패: {e}")
                return total_count, all_books

            soup = BeautifulSoup(resp.text, "html.parser")

            if page == 1:
                for a_tag in soup.select("a"):
                    txt = a_tag.text.strip()
                    if "전체(" in txt or "단행본(" in txt:
                        m = re.search(r'\(([\d,]+)\)', txt)
                        if m:
                            try:
                                total_count = int(m.group(1).replace(",", ""))
                                break
                            except Exception:
                                pass

            book_items = soup.select(".book_dataOuter")
            if not book_items:
                break

            if total_count == 0:
                total_count = len(book_items)

            for item in book_items:
                book = BookInfo(region="서울특별시")

                title_tag = item.select_one(".book_name a span.title")
                if title_tag:
                    book.title = title_tag.text.strip()

                author_tag = item.select_one(".info01")
                if author_tag:
                    book.author = author_tag.text.strip()

                info02_spans = item.select(".info02 span")
                if len(info02_spans) >= 1:
                    book.publisher = info02_spans[0].text.strip()
                if len(info02_spans) >= 3:
                    book.call_number = info02_spans[2].text.strip()
                elif len(info02_spans) == 2:
                    book.call_number = info02_spans[1].text.strip()

                info03_spans = item.select(".info03 span")
                if len(info03_spans) >= 1:
                    lib_name = info03_spans[0].text.strip()
                    book.library = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
                if len(info03_spans) >= 2:
                    book.location = info03_spans[1].text.strip()

                if not book.library:
                    book.library = "송파구립도서관"
                
                if "도서관도서관" in book.library:
                    book.library = book.library.replace("도서관도서관", "도서관")

                if book.title:
                    all_books.append(book)

            if len(all_books) >= total_count or len(book_items) == 0:
                break
            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("송파구립도서관", SongpaScraper, metro_name="서울특별시")


class DongjakScraper(LibraryScraper):
    """동작구립도서관 스크래퍼 (lib.dongjak.go.kr - 포털 검색 연동)"""
    def __init__(self):
        super().__init__(
            region_name="동작구립도서관",
            base_url="https://lib.dongjak.go.kr/dj/intro/search/index.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111'
        }

        all_books = []
        total_count = 0
        page = 1

        while True:
            payload_full = [
                ("menu_idx", "111"),
                ("search_type", "TITLE"),
                ("search_text", query),
                ("libraryCodes", "ALL"),
                ("_libraryCodes", "on"),
                ("libraryCodes", "GuALL"),
                ("_libraryCodes", "on"),
                ("libraryCodes", "DongALL"),
                ("_libraryCodes", "on"),
                ("libraryCodes", "SiALL"),
                ("_libraryCodes", "on"),
                ("booktype", "BOOK"),
                ("viewPage", str(page)),
                ("rowCount", "100")
            ]

            try:
                if page == 1:
                    self._session.get("https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111", headers=headers, timeout=8, verify=False)
                r = self._session.post(self.base_url, data=payload_full, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
            except Exception as e:
                print(f"  [오류] 동작구립도서관 검색 실패: {e}")
                return total_count, all_books

            soup = BeautifulSoup(r.text, "html.parser")
            
            if page == 1:
                cnt_info = soup.select_one("div.search-info")
                if cnt_info:
                    m = re.search(r"총\s*(\d+)건", cnt_info.text)
                    if m:
                        total_count = int(m.group(1))

            items = soup.select("ul.result-list > li, table tbody tr, div.book-info")
            if not items:
                break

            for item in items:
                title_tag = item.select_one("dt.tit a, td.title a, div.title a")
                if not title_tag:
                    continue
                book_title = title_tag.text.strip()
                
                author_tag = item.select_one("dd.author span, td.author")
                book_author = author_tag.text.strip() if author_tag else ""

                call_no = item.get("callno", "") or ""
                lib_name = item.get("libname", "동작구립도서관") or "동작구립도서관"
                if not lib_name.endswith("도서관"):
                    lib_name += "도서관"

                if book_title:
                    book = BookInfo(region="서울특별시")
                    book.title = book_title
                    book.author = book_author
                    book.library = lib_name
                    book.call_number = call_no
                    all_books.append(book)

            if len(all_books) >= total_count or len(items) == 0:
                break
            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("동작구립도서관", DongjakScraper, metro_name="서울특별시")


class SeochoScraper(LibraryScraper):
    """서초구립도서관 스크래퍼 (seocholib.or.kr - REST API & 2차 소장 연동)"""
    def __init__(self):
        super().__init__(
            region_name="서초구립도서관",
            base_url="https://www.seocholib.or.kr/api/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.seocholib.or.kr/'
        }

        all_books = []
        total_count = 0
        page = 1

        while True:
            payload = {
                "searchKeyword": query,
                "page": page,
                "display": 100
            }

            try:
                r = self._session.post(self.base_url, json=payload, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  [오류] 서초구립도서관 1차 검색 실패: {e}")
                return total_count, all_books

            contents = data.get("contents", {})
            if page == 1:
                total_count = contents.get("totalCount", 0)

            items = contents.get("bookList", [])
            if not items:
                break

            for item in items:
                raw_title = item.get("originalTitle") or item.get("title", "")
                book_title = re.sub(r"<[^>]+>", "", raw_title).strip()
                
                raw_author = item.get("originalAuthor") or item.get("author", "")
                book_author = re.sub(r"\s*지음|\s*저\.?", "", raw_author).strip()

                species_key = item.get("speciesKey", "")
                manage_codes_str = item.get("manageCode", "")

                if species_key and manage_codes_str:
                    s_key = species_key.split(",")[0].strip()
                    m_codes = [mc.strip() for mc in manage_codes_str.split(",") if mc.strip()]

                    for mcode in m_codes:
                        url_det = f"https://www.seocholib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={s_key}&manageCode={mcode}"
                        try:
                            r_det = self._session.get(url_det, headers=headers, timeout=6, verify=False)
                            if r_det.status_code == 200:
                                det_json = r_det.json()
                                col_list = det_json.get("contents", {}).get("collectionList", [])
                                for col in col_list:
                                    lib_name = col.get("libName", "").strip() or "서초구립도서관"
                                    if not lib_name.endswith("도서관"):
                                        lib_name += "도서관"
                                    
                                    call_no = col.get("callNo", "").strip()
                                    shelf_loc = col.get("shelfLocName", "").strip()

                                    if "도서관도서관" in lib_name:
                                        lib_name = lib_name.replace("도서관도서관", "도서관")

                                    book = BookInfo(region="서울특별시")
                                    book.title = book_title
                                    book.author = book_author
                                    book.library = lib_name
                                    book.call_number = call_no
                                    book.location = shelf_loc
                                    all_books.append(book)
                        except Exception:
                            pass
                else:
                    lib_name = item.get("libName", "서초구립도서관")
                    if not lib_name.endswith("도서관"):
                        lib_name += "도서관"
                    call_no = item.get("callNo", "").strip()
                    location = item.get("shelfLocName", "").strip()
                    book = BookInfo(region="서울특별시")
                    book.title = book_title
                    book.author = book_author
                    book.library = lib_name
                    book.call_number = call_no
                    book.location = location
                    all_books.append(book)

            if len(all_books) >= total_count or len(items) == 0:
                break
            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("서초구립도서관", SeochoScraper, metro_name="서울특별시")


class DongdaemunScraper(LibraryScraper):
    """동대문구립도서관 스크래퍼 (www.l4d.or.kr - JNET 연동)"""
    def __init__(self):
        super().__init__(
            region_name="동대문구립도서관",
            base_url="https://www.l4d.or.kr/intro/menu/10096/program/30010/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.l4d.or.kr/intro/menu/10096/program/30010/plusSearchSimple.do'
        }

        try:
            self._session.get("https://www.l4d.or.kr/intro/menu/10096/program/30010/plusSearchSimple.do", headers=headers, timeout=8, verify=False)
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 동대문구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("dl.bookDataWrap")
        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            author_tag = item.select_one("dd.author span")
            book_author = author_tag.text.strip() if author_tag else ""
            book_author = re.sub(r"^저자\s*:\s*", "", book_author).strip()

            call_no = ""
            for span in item.select("dd.data span"):
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").strip()
                    break

            lib_name = ""
            for span in item.select("dd.site span"):
                txt = span.text.strip()
                if "관" in txt or "도서관" in txt:
                    lib_name = txt.replace("도서관", "").replace("도서", "").replace("관", "").replace(":", "").strip() + "도서관"
                    break

            if not lib_name or lib_name == "도서관":
                lib_name = "동대문구립도서관"

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("동대문구립도서관", DongdaemunScraper, metro_name="서울특별시")


class NowonScraper(LibraryScraper):
    """노원구립도서관 스크래퍼 (www.nowonlib.kr - REST API & 소장 상세 2차 연동)"""
    def __init__(self):
        super().__init__(
            region_name="노원구립도서관",
            base_url="https://www.nowonlib.kr/api/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.nowonlib.kr/'
        }

        all_books = []
        total_count = 0
        page = 1

        while True:
            payload = {
                "searchKeyword": query,
                "page": str(page),
                "display": "100"
            }

            try:
                r = self._session.post(self.base_url, json=payload, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  [오류] 노원구립도서관 1차 검색 실패: {e}")
                return total_count, all_books

            contents = data.get("contents", {})
            if page == 1:
                total_count = contents.get("totalCount", 0)

            items = contents.get("bookList", [])
            if not items:
                break

            for item in items:
                raw_title = item.get("originalTitle") or item.get("title", "")
                book_title = re.sub(r"<[^>]+>", "", raw_title).strip()

                raw_author = item.get("originalAuthor") or item.get("author", "")
                book_author = re.sub(r"\s*지음|\s*저\.?", "", raw_author).strip()

                species_key = item.get("speciesKey", "")
                manage_codes_str = item.get("manageCode", "")

                if not species_key or not manage_codes_str:
                    continue

                s_key = species_key.split(",")[0].strip()
                m_codes = [mc.strip() for mc in manage_codes_str.split(",") if mc.strip()]

                # 2차 상세 소장정보 요청 (각 관별 청구기호/위치 수집)
                for mcode in m_codes:
                    url_det = f"https://www.nowonlib.kr/api/bookDetail/bookCollection/MOMM?speciesKey={s_key}&manageCode={mcode}"
                    try:
                        r_det = self._session.get(url_det, headers=headers, timeout=6, verify=False)
                        if r_det.status_code == 200:
                            det_json = r_det.json()
                            col_list = det_json.get("contents", {}).get("collectionList", [])
                            for col in col_list:
                                lib_name = col.get("libName", "").strip() or "노원구립도서관"
                                if not lib_name.endswith("도서관"):
                                    lib_name += "도서관"
                                
                                call_no = col.get("callNo", "").strip()
                                shelf_loc = col.get("shelfLocName", "").strip()

                                if "도서관도서관" in lib_name:
                                    lib_name = lib_name.replace("도서관도서관", "도서관")

                                book = BookInfo(region="서울특별시")
                                book.title = book_title
                                book.author = book_author
                                book.library = lib_name
                                book.call_number = call_no
                                book.location = shelf_loc
                                all_books.append(book)
                    except Exception:
                        pass

            if len(all_books) >= total_count or len(items) == 0:
                break
            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("노원구립도서관", NowonScraper, metro_name="서울특별시")


class DobongScraper(LibraryScraper):
    """도봉구립도서관 스크래퍼 (www.unilib.dobong.kr - JNET 연동)"""
    def __init__(self):
        super().__init__(
            region_name="도봉구립도서관",
            base_url="https://www.unilib.dobong.kr/site/search/search00.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        params = {
            "cmd_name": "bookandnonbooksearch",
            "search_type": "detail",
            "manage_code": "MA,MB,MC,ME,MG,MJ,MF,MH,SA,MD,SB,SL,SM,SN,SO,SP,SK,SQ,SR,SS,ST,SU,SG,SH,SC",
            "search_txt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.unilib.dobong.kr/main.do'
        }

        try:
            r = self._session.get(self.base_url, params=params, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 도봉구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        
        items = soup.select("div.book_info_w")
        books = []
        for item in items:
            tit_div = item.select_one("div.tit")
            if not tit_div:
                continue
            full_tit = tit_div.text.strip()

            parts = full_tit.split(maxsplit=1)
            if len(parts) == 2:
                lib_name = parts[0].strip() + "도서관"
                book_title = parts[1].strip()
            else:
                lib_name = "도봉구립도서관"
                book_title = full_tit

            cont_div = item.select_one("div.cont")
            cont_txt = cont_div.text.strip() if cont_div else ""
            cont_clean = re.sub(r"\s+", " ", cont_txt)

            book_author = ""
            m_auth = re.search(r"저자\s+([^\s]+(?:\s+[^\s]+)*?)(?=\s+발행처|\s+발행년|\s+자료위치|$)", cont_clean)
            if m_auth:
                book_author = m_auth.group(1).strip()

            location = ""
            m_loc = re.search(r"자료위치\s+([^\s]+(?:\s+[^\s]+)*?)(?=\s+등록번호|\s+청구기호|$)", cont_clean)
            if m_loc:
                location = m_loc.group(1).strip()

            call_no = ""
            call_tag = item.select_one("input[name='mb_callno_info']")
            if call_tag:
                call_no = call_tag.get("value", "").strip()
            else:
                for dl in item.select("dl"):
                    dt = dl.select_one("dt")
                    dd = dl.select_one("dd")
                    if dt and dd and "청구기호" in dt.text:
                        call_no = dd.text.strip()
                        break

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.location = location
                book.call_number = call_no
                books.append(book)

        return len(books), books

register_scraper("도봉구립도서관", DobongScraper, metro_name="서울특별시")


class YeongdeungpoScraper(LibraryScraper):
    """영등포구립도서관 스크래퍼 (www.ydplib.or.kr - JNET 연동)"""
    def __init__(self):
        super().__init__(
            region_name="영등포구립도서관",
            base_url="https://www.ydplib.or.kr/intro/menu/10006/program/30001/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.ydplib.or.kr/intro/menu/10006/program/30001/plusSearchSimple.do'
        }

        try:
            self._session.get("https://www.ydplib.or.kr/intro/menu/10006/program/30001/plusSearchSimple.do", headers=headers, timeout=8, verify=False)
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 영등포구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        
        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("dl.bookDataWrap")
        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            author_tag = item.select_one("dd.author span")
            book_author = author_tag.text.strip() if author_tag else ""
            book_author = re.sub(r"^저자\s*:\s*", "", book_author).strip()

            call_no = ""
            for span in item.select("dd.data span"):
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치출력", "").strip()
                    break

            lib_name = ""
            for span in item.select("dd.site span"):
                txt = span.text.strip()
                if "관" in txt or "도서관" in txt:
                    lib_name = txt.replace("도서관", "").replace("도서", "").replace("관", "").replace(":", "").strip() + "도서관"
                    break

            if not lib_name or lib_name == "도서관":
                lib_name = "영등포구립도서관"

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("영등포구립도서관", YeongdeungpoScraper, metro_name="서울특별시")


class JungnangScraper(LibraryScraper):
    """중랑구립도서관 스크래퍼 (www.jungnanglib.seoul.kr - JNET 연동)"""
    def __init__(self):
        super().__init__(
            region_name="중랑구립도서관",
            base_url="https://www.jungnanglib.seoul.kr/intro/menu/10003/program/30001/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.jungnanglib.seoul.kr/intro/menu/10003/program/30001/searchSimple.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 중랑구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        
        cnt_tag = soup.select_one("div.result_screen")
        total_count = 0
        if cnt_tag:
            m = re.search(r"총\s*(\d+)\s*건", cnt_tag.text)
            if m:
                total_count = int(m.group(1))

        items = soup.select("div.book_dataInner")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, p.tit a, span.tit")
            if tit_tag:
                book_title = tit_tag.text.strip()
            else:
                txt_full = item.text.strip()
                m_tit = re.search(r"단행본\s+([^\n\r]+)", txt_full)
                book_title = m_tit.group(1).strip() if m_tit else ""

            if not book_title:
                continue

            txt = item.text.strip().replace("\n", " ")
            lib_name = "중랑구립도서관"
            m_lib = re.search(r"\[([^\]]+)\](?:\s*종합자료실|\s*어린이자료실|\s*자료실|$)", txt)
            if m_lib:
                lib_name = m_lib.group(1).strip() + "도서관"

            m_call = re.search(r"([A-Z]{1,3}\s*\d{3}\.\d+-[^\s]+)", txt)
            call_no = m_call.group(1).strip() if m_call else ""

            book = BookInfo(region="서울특별시")
            book.title = book_title
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books


register_scraper("중랑구립도서관", JungnangScraper, metro_name="서울특별시")


class JongnoScraper(LibraryScraper):
    """종로구립도서관 스크래퍼 (lib.jongno.go.kr - 포털 검색 연동)"""
    def __init__(self):
        super().__init__(
            region_name="종로구립도서관",
            base_url="https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "library": "ALL",
            "search_type": "normal",
            "search_value": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://lib.jongno.go.kr/'
        }

        try:
            r = self._session.post(self.base_url, data=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 종로구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")
        
        items = soup.select("ul.book_list > li, li.book_top_info, div.book_name")
        books = []
        for item in items:
            full_txt = item.text.strip()
            if not full_txt:
                continue

            m_lib = re.search(r"\[([^\]]+)\]", full_txt)
            if m_lib:
                raw_lib = m_lib.group(1).strip()
                lib_name = raw_lib if raw_lib.endswith("도서관") or "북카페" in raw_lib else raw_lib + "도서관"
            else:
                lib_name = "종로구립도서관"

            book_title = re.sub(r"\[[^\]]+\]", "", full_txt).strip()
            book_title = re.sub(r"\s*대출가능.*|\s*대출불가.*", "", book_title).strip()

            call_no = ""
            m_call = re.search(r"([A-Za-z0-9가-힣\s._\-]{3,15}\s+\d{3}(?:\.\d+)?-[^\s]+)", full_txt)
            if not m_call:
                m_call = re.search(r"(\d{3}(?:\.\d+)?-[^\s]+)", full_txt)
            if m_call:
                call_no = m_call.group(1).strip()

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return len(books), books

register_scraper("종로구립도서관", JongnoScraper, metro_name="서울특별시")


class GwanakScraper(LibraryScraper):
    """관악구립도서관 스크래퍼 (lib.gwanak.go.kr - JNET dl.bookDataWrap)"""
    def __init__(self):
        super().__init__(
            region_name="관악구립도서관",
            base_url="https://lib.gwanak.go.kr/galib/menu/10003/program/30001/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://lib.gwanak.go.kr/galib/menu/10003/program/30001/searchSimple.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 관악구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("dl.bookDataWrap")
        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            author_tag = item.select_one("dd.author span")
            book_author = author_tag.text.strip() if author_tag else ""
            book_author = re.sub(r"^저자\s*:\s*", "", book_author).strip()

            call_no = ""
            lib_name = "관악구립도서관"
            for span in item.select("dd.data span, dd.site span"):
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").strip()
                elif any(k in txt for k in ["도서관", "문고", "작은"]):
                    lib_name = txt.strip()

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("관악구립도서관", GwanakScraper, metro_name="서울특별시")


class YongsanScraper(LibraryScraper):
    """용산구립도서관 스크래퍼 (yslibrary.or.kr - JNET dl.bookDataWrap)"""
    def __init__(self):
        super().__init__(
            region_name="용산구립도서관",
            base_url="https://www.yslibrary.or.kr/intro/menu/10003/program/30001/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.yslibrary.or.kr/intro/searchSimple.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 용산구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("dl.bookDataWrap")
        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            author_tag = item.select_one("dd.author span")
            book_author = author_tag.text.strip() if author_tag else ""
            book_author = re.sub(r"^저자\s*:\s*", "", book_author).strip()

            call_no = ""
            lib_name = "용산구립도서관"
            for span in item.select("dd.data span, dd.site span"):
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").strip()
                elif any(k in txt for k in ["도서관", "문고", "작은"]):
                    lib_name = txt.strip()

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("용산구립도서관", YongsanScraper, metro_name="서울특별시")


class JungguScraper(LibraryScraper):
    """중구립도서관 스크래퍼 (junggulib.or.kr - JNET div.book_dataInner)"""
    def __init__(self):
        super().__init__(
            region_name="중구립도서관",
            base_url="https://www.junggulib.or.kr/SJGL/program/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.junggulib.or.kr/SJGL/program/searchSimple.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 중구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("div.result_screen")
        total_count = 0
        if cnt_tag:
            m = re.search(r"총\s*(\d+)\s*건", cnt_tag.text)
            if m:
                total_count = int(m.group(1))

        items = soup.select("div.book_dataInner")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, p.tit a, span.tit")
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
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|$)", txt)
            if not m_auth:
                m_auth = re.search(r"([^\s]+\s+(?:지음|저|편저|글))", txt)
            if m_auth:
                book_author = m_auth.group(1).strip()

            lib_name = "중구립도서관"
            m_lib = re.search(r"\[([^\]]+)\]", txt)
            if m_lib:
                raw = m_lib.group(1).strip()
                lib_name = raw if raw.endswith("도서관") else raw + "도서관"

            call_no = ""
            m_call = re.search(r"([A-Za-z0-9가-힣\s._\-]{1,15}\s*\d{3}(?:\.\d+)?[-\s][^\s]+?)(?=위치출력|\s+위치|\s+대출|$)", txt)
            if not m_call:
                m_call = re.search(r"(\d{3}(?:\.\d+)?[-\s][^\s]+?)(?=위치출력|\s+위치|\s+대출|$)", txt)
            if m_call:
                call_no = m_call.group(1).strip()

            book = BookInfo(region="서울특별시")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("중구립도서관", JungguScraper, metro_name="서울특별시")


class GeumcheonScraper(LibraryScraper):
    """금천구립도서관 스크래퍼 (geumcheonlib.seoul.kr - AJAX JSON API)"""
    def __init__(self):
        super().__init__(
            region_name="금천구립도서관",
            base_url="https://geumcheonlib.seoul.kr/book/bookSearchList"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title

        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://geumcheonlib.seoul.kr/geumcheonlib/uce/search/totalList.do?selfId=1097',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        try:
            self._session.get(
                "https://geumcheonlib.seoul.kr/geumcheonlib/uce/search/totalList.do?selfId=1097",
                headers={'User-Agent': self._headers['User-Agent']}, timeout=8, verify=False
            )
            r = self._session.post(self.base_url, data={
                "searchKeyword": query,
                "page": 1,
                "article": "TITLE",
                "display": 20,
                "manageCode": "ALL",
            }, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 금천구립도서관 검색 실패: {e}")
            return 0, []

        try:
            data = r.json()
        except Exception:
            return 0, []

        total_count = data.get("totalCount", 0)
        book_list = data.get("bookList", [])

        manage_map = {}
        for lib in data.get("searchLibList", []):
            manage_map[lib.get("manageCode", "")] = lib.get("libName", lib.get("manageName", ""))

        books = []
        for item in book_list:
            book_title = item.get("titleStatement", item.get("title", ""))
            book_title = re.sub(r"<[^>]+>", "", book_title).strip()

            book_author = item.get("author", "")
            call_no = item.get("callNo", "")

            mc = item.get("manageCode", "")
            lib_name = item.get("libName", manage_map.get(mc, ""))
            if lib_name:
                lib_name = lib_name + "도서관" if not lib_name.endswith("도서관") else lib_name
            else:
                lib_name = "금천구립도서관"

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("금천구립도서관", GeumcheonScraper, metro_name="서울특별시")


class SeodaemunScraper(LibraryScraper):
    """서대문구립도서관 스크래퍼 (lib.sdm.or.kr - JNET 연동)"""
    def __init__(self):
        super().__init__(
            region_name="서대문구립도서관",
            base_url="https://lib.sdm.or.kr/sdmlib/menu/10003/program/30001/searchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://lib.sdm.or.kr/sdmlib/menu/10003/program/30001/searchSimple.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 서대문구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("div.result_screen, span.themeFC, b.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"총\s*(\d+)\s*건", cnt_tag.text)
            if not m:
                m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(1) if m.lastindex else m.group(0))

        items = soup.select("div.book_dataInner")
        books = []
        for item in items:
            tit_tag = item.select_one("dt.tit a, a.tit, p.tit a, span.tit")
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
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행|$)", txt)
            if not m_auth:
                m_auth = re.search(r"([^\s]+\s+(?:지음|저|편저|글))", txt)
            if m_auth:
                book_author = m_auth.group(1).strip()

            lib_name = "서대문구립도서관"
            m_lib = re.search(r"\[([^\]]+)\]", txt)
            if m_lib:
                raw = m_lib.group(1).strip()
                if raw == "공":
                    lib_name = "이진아기념도서관"
                else:
                    lib_name = raw if raw.endswith("도서관") or "새싹" in raw or "새롬" in raw else raw + "도서관"

            call_no = ""
            m_call = re.search(r"([A-Za-z0-9가-힣\s._\-]{1,15}\s*\d{3}(?:\.\d+)?[-\s][^\s]+?)(?=위치출력|\s+위치|\s+대출|$)", txt)
            if not m_call:
                m_call = re.search(r"(\d{3}(?:\.\d+)?[-\s][^\s]+?)(?=위치출력|\s+위치|\s+대출|$)", txt)
            if m_call:
                call_no = m_call.group(1).strip()

            book = BookInfo(region="서울특별시")
            book.title = book_title
            book.author = book_author
            book.library = lib_name
            book.call_number = call_no
            books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("서대문구립도서관", SeodaemunScraper, metro_name="서울특별시")


class SeongdongScraper(LibraryScraper):
    """성동구립도서관 스크래퍼 (www.sdlib.or.kr - JNET search00.do)"""
    def __init__(self):
        super().__init__(
            region_name="성동구립도서관",
            base_url="https://www.sdlib.or.kr/SD/site/search/search00.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        payload = {
            "cmd_name": "bookandnonbooksearch",
            "search_type": "detail",
            "use_facet": "N",
            "main_type": "Y",
            "search_txt": query
        }
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Referer': 'https://www.sdlib.or.kr/SD/main.do'
        }

        try:
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 성동구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select("div.book_info_w")
        books = []
        for item in items:
            full_tit = ""
            for a in item.select("a[href*='species_key'], a[href*='manage_code']"):
                if a.text.strip():
                    full_tit = a.text.strip()
                    break

            if not full_tit:
                continue

            m_lib = re.search(r"\[([^\]]+)\]", full_tit)
            if m_lib:
                raw_lib = m_lib.group(1).strip()
                lib_name = raw_lib if raw_lib.endswith("도서관") else raw_lib + "도서관"
            else:
                lib_name = "성동구립도서관"

            book_title = re.sub(r"\[[^\]]+\]", "", full_tit).strip()
            book_title = re.sub(r"\s*대출가능.*|\s*대출불가.*", "", book_title).strip()

            cont_txt = item.text.strip().replace("\n", " ")
            cont_clean = re.sub(r"\s+", " ", cont_txt)

            book_author = ""
            m_auth = re.search(r"저자\s*:?\s*([^\n]+?)(?=\s*발행처|\s*발행년|\s*자료위치|\s*매체구분|$)", cont_clean)
            if m_auth:
                book_author = m_auth.group(1).strip()

            location = ""
            m_loc = re.search(r"자료위치\s*:?\s*([^\n]+?)(?=\s*청구기호|\s*등록번호|\s*상태|\s*책누리|\s*북토리지|\s*관심도서|$)", cont_clean)
            if m_loc:
                location = m_loc.group(1).strip()
                location = re.sub(r"\s*책누리.*|\s*북토리지.*|\s*관심도서.*", "", location).strip()

            call_no = ""
            m_call = re.search(r"청구기호\s*([^\s]+)", cont_clean)
            if m_call:
                call_no = m_call.group(1).strip()

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.location = location
                book.call_number = call_no
                books.append(book)

        return len(books), books

register_scraper("성동구립도서관", SeongdongScraper, metro_name="서울특별시")


class EunpyeongScraper(LibraryScraper):
    """은평구립도서관 스크래퍼 (www.eplib.or.kr - Vue REST API & 2차 소장 연동)"""
    def __init__(self):
        super().__init__(
            region_name="은평구립도서관",
            base_url="https://www.eplib.or.kr/api/search"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        query = f"{title} {author}".strip() if author else title
        headers = {
            'User-Agent': self._headers['User-Agent'],
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.eplib.or.kr/unified/search.asp'
        }

        all_books = []
        total_count = 0
        page = 1

        while True:
            payload = {
                "searchKeyword": query,
                "page": page,
                "display": 100,
                "selectedLibraries": ["ALL"]
            }

            try:
                r = self._session.post(self.base_url, json=payload, headers=headers, timeout=12, verify=False)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"  [오류] 은평구립도서관 1차 검색 실패: {e}")
                return total_count, all_books

            contents = data.get("contents", {})
            if page == 1:
                total_count = contents.get("totalCount", 0)

            book_list = contents.get("bookList", [])
            if not book_list:
                break

            manage_codes_default = ["MA", "MB", "MC", "MD", "ME", "MF", "MG", "MH", "MI", "MJ", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ"]

            for item in book_list:
                raw_title = item.get("title", "")
                book_title = re.sub(r"<[^>]+>", "", raw_title).strip()
                book_author = item.get("author", "")

                species_key = item.get("speciesKey", "")
                manage_codes_str = item.get("manageCode", "")

                if species_key:
                    s_key = species_key.split(",")[0].strip()
                    m_codes = [mc.strip() for mc in manage_codes_str.split(",") if mc.strip()] if manage_codes_str else manage_codes_default

                    for mcode in m_codes:
                        url_det = f"https://www.eplib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={s_key}&manageCode={mcode}"
                        try:
                            r_det = self._session.get(url_det, headers=headers, timeout=5, verify=False)
                            if r_det.status_code == 200:
                                det_json = r_det.json()
                                col_list = det_json.get("contents", {}).get("collectionList", [])
                                for col in col_list:
                                    lib_name = col.get("libName", "").strip() or "은평구립도서관"
                                    if not lib_name.endswith("도서관"):
                                        lib_name += "도서관"
                                    
                                    call_no = col.get("callNo", "").strip()
                                    shelf_loc = col.get("shelfLocName", "").strip()

                                    if "도서관도서관" in lib_name:
                                        lib_name = lib_name.replace("도서관도서관", "도서관")

                                    book = BookInfo(region="서울특별시")
                                    book.title = book_title
                                    book.author = book_author
                                    book.library = lib_name
                                    book.call_number = call_no
                                    book.location = shelf_loc
                                    all_books.append(book)
                        except Exception:
                            pass
                else:
                    lib_names = item.get("libName", [])
                    lib_name = ", ".join(lib_names) if isinstance(lib_names, list) else str(lib_names or "은평구립도서관")
                    book = BookInfo(region="서울특별시")
                    book.title = book_title
                    book.author = book_author
                    book.library = lib_name
                    all_books.append(book)

            if len(all_books) >= total_count or len(book_list) == 0:
                break
            page += 1

        return total_count if total_count > 0 else len(all_books), all_books

register_scraper("은평구립도서관", EunpyeongScraper, metro_name="서울특별시")


class GwangjinScraper(LibraryScraper):
    """광진구립도서관 스크래퍼 (www.gwangjinlib.seoul.kr - JNET plusSearchResultList.do)"""
    def __init__(self):
        super().__init__(
            region_name="광진구립도서관",
            base_url="https://www.gwangjinlib.seoul.kr/gjinfo/menu/10003/program/30001/plusSearchResultList.do"
        )
        self._session = requests.Session()
        self._session.mount('https://', _SslAdapter())

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
            'Referer': 'https://www.gwangjinlib.seoul.kr/intro.do'
        }

        try:
            self._session.get("https://www.gwangjinlib.seoul.kr/intro.do", headers=headers, timeout=8, verify=False)
            r = self._session.get(self.base_url, params=payload, headers=headers, timeout=12, verify=False)
            r.raise_for_status()
        except Exception as e:
            print(f"  [오류] 광진구립도서관 검색 실패: {e}")
            return 0, []

        soup = BeautifulSoup(r.text, "html.parser")

        cnt_tag = soup.select_one("span.themeFC, b.themeFC, strong.themeFC")
        total_count = 0
        if cnt_tag:
            m = re.search(r"\d+", cnt_tag.text.strip())
            if m:
                total_count = int(m.group(0))

        items = soup.select("dl.bookDataWrap")
        books = []
        for item in items:
            title_tag = item.select_one("dt.tit a")
            if not title_tag:
                continue
            book_title = title_tag.text.strip()
            book_title = re.sub(r"^\d+\.\s*", "", book_title).strip()

            author_tag = item.select_one("dd.author span")
            book_author = author_tag.text.strip() if author_tag else ""
            book_author = re.sub(r"^저자\s*:\s*", "", book_author).strip()

            call_no = ""
            lib_name = "광진구립도서관"
            for span in item.select("dd.data span, dd.site span"):
                txt = span.text.strip()
                if "청구기호" in txt:
                    call_no = txt.replace("청구기호", "").replace(":", "").replace("위치출력", "").strip()
                elif any(k in txt for k in ["도서관", "문고", "작은"]):
                    clean_lib = txt.replace("도서관:", "").replace("도서관 :", "").strip()
                    lib_name = clean_lib if clean_lib.endswith("도서관") else clean_lib + "도서관"

            if book_title:
                book = BookInfo(region="서울특별시")
                book.title = book_title
                book.author = book_author
                book.library = lib_name
                book.call_number = call_no
                books.append(book)

        return total_count if total_count > 0 else len(books), books

register_scraper("광진구립도서관", GwangjinScraper, metro_name="서울특별시")


# ========================================================================
# 미확인 사이트
# ========================================================================

UNIMPLEMENTED_SEOUL = [
    "강동구립도서관", "강북구립도서관",
    "구로구립도서관",
    "마포구립도서관",
    "양천구립도서관"
]

for lib_name in UNIMPLEMENTED_SEOUL:
    class _Scraper(GenericLibraryScraper):
        def __init__(self, lname=lib_name):
            super().__init__(region_name=lname, metro_name="서울특별시")

    register_scraper(lib_name, _Scraper, metro_name="서울특별시")












