def validate_khitan(glyphs, expected_count):
    actual_count = len(glyphs)
    unicode_coverage = sum(1 for g in glyphs if g.get("unicode_value")) / actual_count * 100 if actual_count > 0 else 0
    has_primary_source = any("Unicode" in s["source_name"] for g in glyphs for s in g.get("sources", []))

    return {
        "passed": actual_count >= expected_count and unicode_coverage >= 80 and has_primary_source,
        "details": {
            "glyph_count": actual_count,
            "expected_minimum": expected_count,
            "unicode_coverage_pct": round(unicode_coverage, 2),
            "primary_source_present": has_primary_source
        },
        "recommendations": [] if actual_count >= expected_count else ["Add more glyphs from additional Khitan sources"]
    }
