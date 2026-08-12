"""
범용 공공도서관 스크래퍼 (fallback)
실제 검색 엔드포인트가 확인되지 않은 도서관용.
더미 데이터를 반환하지 않고 정직하게 빈 결과를 반환합니다.
"""
from .base import LibraryScraper, BookInfo


class GenericLibraryScraper(LibraryScraper):
    """
    범용 공공도서관 스크래퍼 (미구현 도서관 대응용)
    실제 검색 엔드포인트가 확인되지 않은 도서관의 경우
    빈 결과를 반환하고 안내 메시지를 출력합니다.
    """

    def __init__(self, region_name: str, metro_name: str = ""):
        self.metro_name = metro_name or "공공도서관"
        super().__init__(
            region_name=region_name,
            base_url=""
        )

    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        print(f"  [안내] '{self.region_name}' 도서관은 아직 검색 엔드포인트가 구현되지 않았습니다.")
        print(f"         해당 도서관 웹사이트를 직접 방문하여 검색해 주세요.")
        return 0, []
