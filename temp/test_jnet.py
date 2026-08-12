"""
jnet 스크래퍼 실제 검색 테스트
"""
import warnings
warnings.filterwarnings("ignore")

from scrapers import get_scraper

# Type A 테스트 (구리시, 과천시)
print("=" * 70)
print(" Type A (searchResultList.do) 실제 검색 테스트")
print("=" * 70)

for city in ["구리시", "과천시"]:
    print(f"\n--- {city} ---")
    scraper = get_scraper(city, "경기도")
    total, books = scraper.search("파이썬")
    print(f"  총 {total}건, 반환 {len(books)}건")
    for b in books[:3]:
        print(f"  [{b.library}] {b.title[:40]} | 청구기호: {b.call_number} | 저자: {b.author[:20]}")

# Type B 테스트 (평택시, 성남시, 남양주시, 포천시, 강남구립)
print("\n" + "=" * 70)
print(" Type B (plusSearchResultList.do) 실제 검색 테스트")
print("=" * 70)

for city in ["평택시", "성남시", "남양주시", "포천시", "강남구립도서관"]:
    print(f"\n--- {city} ---")
    scraper = get_scraper(city, "경기도" if "구립" not in city else "서울특별시")
    total, books = scraper.search("파이썬")
    print(f"  총 {total}건, 반환 {len(books)}건")
    for b in books[:3]:
        print(f"  [{b.library}] {b.title[:40]} | 청구기호: {b.call_number} | 저자: {b.author[:20]}")

# 미구현 도서관 테스트 (빈 결과 확인)
print("\n" + "=" * 70)
print(" 미구현 도서관 테스트 (빈 결과 반환 확인)")
print("=" * 70)

for city in ["수원시", "부천시"]:
    print(f"\n--- {city} ---")
    scraper = get_scraper(city, "경기도")
    total, books = scraper.search("파이썬")
    print(f"  총 {total}건, 반환 {len(books)}건")

# 기존 개별 스크래퍼 동작 확인 (화성, 용인, 안양)
print("\n" + "=" * 70)
print(" 기존 개별 스크래퍼 동작 확인")
print("=" * 70)

for city in ["화성", "용인", "안양"]:
    print(f"\n--- {city} ---")
    scraper = get_scraper(city)
    total, books = scraper.search("파이썬")
    print(f"  총 {total}건, 반환 {len(books)}건")
    for b in books[:2]:
        print(f"  [{b.library}] {b.title[:40]} | 청구기호: {b.call_number}")
