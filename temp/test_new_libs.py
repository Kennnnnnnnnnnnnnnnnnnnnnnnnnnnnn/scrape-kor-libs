"""
신규 연동된 도서관 및 jnet/DLS 스크래퍼 통합 테스트
"""
import warnings
warnings.filterwarnings("ignore")

from scrapers import get_scraper

print("=" * 80)
print("  [TEST] Shin-gyu Yeondong Libs (Suwon, Ansan, Gwangmyeong, Gangnam, Songpa, Ulsan, Seoul, Seongbuk, Anyang, Uijeongbu, Gimpo, Paju, Hanam, Icheon, Yangju, Yeoju, Dongducheon, Gapyeong) Verification")
print("=" * 80)

new_libs = [
    ("수원시", "경기도"),
    ("안산시", "경기도"),
    ("광명시", "경기도"),
    ("의정부시", "경기도"),
    ("김포시", "경기도"),
    ("파주시", "경기도"),
    ("하남시", "경기도"),
    ("이천시", "경기도"),
    ("양주시", "경기도"),
    ("여주시", "경기도"),
    ("동두천시", "경기도"),
    ("가평군", "경기도"),
    ("의왕시", "경기도"),
    ("안성시", "경기도"),
    ("연천군", "경기도"),
    ("군포시", "경기도"),
    ("시흥시", "경기도"),
    ("부천시", "경기도"),
    ("동작구립도서관", "서울특별시"),
    ("서초구립도서관", "서울특별시"),
    ("동대문구립도서관", "서울특별시"),
    ("노원구립도서관", "서울특별시"),
    ("도봉구립도서관", "서울특별시"),
    ("영등포구립도서관", "서울특별시"),
    ("중랑구립도서관", "서울특별시"),
    ("종로구립도서관", "서울특별시"),
    ("관악구립도서관", "서울특별시"),
    ("용산구립도서관", "서울특별시"),
    ("중구립도서관", "서울특별시"),
    ("금천구립도서관", "서울특별시"),
    ("서대문구립도서관", "서울특별시"),
    ("성동구립도서관", "서울특별시"),
    ("은평구립도서관", "서울특별시"),
    ("광진구립도서관", "서울특별시"),
    ("인천광역시교육청도서관", "인천광역시"),
    ("강남구립도서관", "서울특별시"),
    ("송파구립도서관", "서울특별시"),
    ("안양시", "경기도"),
    ("울산도서관", "울산광역시"),
    ("서울도서관", "서울특별시"),
    ("성북구립도서관", "서울특별시")
]

for name, metro in new_libs:
    print(f"\n--- [{metro}] {name} ---")
    try:
        scraper = get_scraper(name, metro)
        total, books = scraper.search("파이썬")
        print(f"  검색결과: 총 {total}건, 반환 {len(books)}건")
        for b in books[:3]:
            print(f"  [{b.library}] {b.title[:45]} | 청구기호: {b.call_number} | 저자: {b.author[:20]}")
    except Exception as e:
        print(f"  [오류] 테스트 실패: {e}")
