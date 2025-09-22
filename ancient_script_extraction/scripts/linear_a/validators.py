def validate_linear_a(glyphs, expected_count):
    actual_count = len(glyphs)
    image_coverage = sum(1 for g in glyphs if g.get("character_image")) / actual_count * 100 if actual_count > 0 else 0
    has_primary_source = any("SigLA" in s["source_name"] for g in glyphs for s in g.get("sources", []))

    return {
        "passed": actual_count >= expected_count and image_coverage >= 70 and has_primary_source,
        "details": {
            "glyph_count": actual_count,
            "expected_minimum": expected_count,
            "image_coverage_pct": round(image_coverage, 2),
            "primary_source_present": has_primary_source
        },
        "recommendations": [] if actual_count >= expected_count else ["Add more glyphs from GORILA or Mnamon"]
    }
