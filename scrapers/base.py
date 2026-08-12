"""
공공도서관 도서 검색 - 기본 클래스 및 데이터 모델
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BookInfo:
    """검색된 도서 정보"""
    title: str = ""        # 책 이름
    author: str = ""       # 저자
    region: str = ""       # 지역
    library: str = ""      # 공공도서관
    location: str = ""     # 도서관 내 열람실
    call_number: str = ""  # 청구기호
    has_audio: str = ""    # 음원 여부


class LibraryScraper(ABC):
    """
    공공도서관 스크래퍼 추상 클래스.
    새로운 지역을 추가하려면 이 클래스를 상속하여 구현합니다.
    """

    def __init__(self, region_name: str, base_url: str):
        self.region_name = region_name
        self.base_url = base_url
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/126.0.0.0 Safari/537.36',
        }

    @abstractmethod
    def search(self, title: str, author: str = "") -> tuple[int, list[BookInfo]]:
        """
        도서를 검색합니다.

        Args:
            title: 책 제목 (검색어)
            author: 저자 (선택, 빈 문자열이면 무시)

        Returns:
            (총 검색 결과 수, BookInfo 리스트)
        """
        pass
