from scrapers import get_scraper, METRO_MAP

seoul_libs = METRO_MAP.get("서울특별시", [])
print(f"Testing {len(seoul_libs)} libraries in 서울특별시...\n")

results = []

for lib_name in seoul_libs:
    try:
        scraper = get_scraper(lib_name, "서울특별시")
        total, books = scraper.search("파친코")
        
        has_call_no = sum(1 for b in books if b.call_number.strip())
        no_call_no = sum(1 for b in books if not b.call_number.strip())
        
        sample_call_nos = [b.call_number for b in books if b.call_number.strip()][:2]
        
        status = "OK" if has_call_no > 0 else ("EMPTY_CALLNO" if len(books) > 0 else "NO_BOOKS")
        
        results.append({
            "name": lib_name,
            "class": scraper.__class__.__name__,
            "total": total,
            "parsed": len(books),
            "has_call_no": has_call_no,
            "no_call_no": no_call_no,
            "sample_call_no": sample_call_nos,
            "status": status
        })
        print(f"[{status}] {lib_name} ({scraper.__class__.__name__}): Total={total}, Parsed={len(books)}, HasCallNo={has_call_no}, Samples={sample_call_nos}")
    except Exception as e:
        print(f"[ERROR] {lib_name}: {e}")
        results.append({
            "name": lib_name,
            "status": f"ERROR: {e}"
        })

print("\n" + "=" * 70)
print("SUMMARY OF ISSUES (No Call Number when Books exist):")
issues = [r for r in results if r.get("status") == "EMPTY_CALLNO"]
if not issues:
    print("NONE! All scrapers with books returned valid call numbers!")
else:
    for r in issues:
        print(f" - {r['name']} ({r['class']}): Parsed {r['parsed']} books, BUT 0 call numbers!")
