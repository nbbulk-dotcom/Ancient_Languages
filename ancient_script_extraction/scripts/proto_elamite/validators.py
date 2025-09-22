def validate_proto_elamite(glyphs, expected_count):
    actual_count = len(glyphs)
    m_code_coverage = sum(1 for g in glyphs if g.get("sign_id", "").startswith("M")) / actual_count * 100 if actual_count > 0 else 0
    has_primary_source = any("CDLI" in s["source_name"] for g in glyphs for s in g.get("sources", []))

    return {
        "passed": actual_count >= expected_count and m_code_coverage >= 90 and has_primary_source,
        "details": {
            "glyph_count": actual_count,
            "expected_minimum": expected_count,
            "m_code_coverage_pct": round(m_code_coverage, 2),
            "primary_source_present": has_primary_source
        },
        "recommendations": [] if actual_count >= expected_count else ["Add more tablets from CDLI corpus"]
    }
