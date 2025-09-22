import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.http_client import rate_limited_get, set_rate_limits
from utils.saver import save_json, save_csv, save_image
from utils.logger import log_event
from utils.dedupe import deduplicate_glyphs
from scripts.khitan.khitan_parsers import parse_unicode_block, parse_babelstone
from scripts.khitan.validators import validate_khitan

def run_khitan_extraction(config, outdir):
    set_rate_limits(config.get('rate_limits', {}))
    expected_count = config['expected_counts']['KhitanLargeScript']
    
    khitan_dir = os.path.join(outdir, "KhitanLargeScript")
    os.makedirs(khitan_dir, exist_ok=True)
    os.makedirs(os.path.join(khitan_dir, "glyph_images"), exist_ok=True)

    log_event("Starting Khitan Large Script extraction", os.path.join(outdir, "extraction_log.txt"))

    parsed = []
    
    try:
        unicode_glyphs = parse_unicode_block("U+18B00", "U+18CFF")
        parsed.extend(unicode_glyphs)
        log_event(f"Extracted {len(unicode_glyphs)} glyphs from Unicode block", os.path.join(outdir, "extraction_log.txt"))
    except Exception as e:
        log_event(f"Unicode block extraction failed: {str(e)}", os.path.join(outdir, "extraction_log.txt"))

    try:
        babelstone_url = config['sources']['KhitanLargeScript'][1]['url']
        babelstone_glyphs = parse_babelstone(babelstone_url)
        parsed.extend(babelstone_glyphs)
        log_event(f"Extracted {len(babelstone_glyphs)} glyphs from BabelStone", os.path.join(outdir, "extraction_log.txt"))
    except Exception as e:
        log_event(f"BabelStone extraction failed: {str(e)}", os.path.join(outdir, "extraction_log.txt"))

    unique_glyphs = deduplicate_glyphs(parsed)

    json_path = os.path.join(khitan_dir, "KhitanLargeScript_complete_glyphs.json")
    csv_path = os.path.join(khitan_dir, "KhitanLargeScript_complete_glyphs.csv")
    save_json(unique_glyphs, json_path)
    
    if unique_glyphs:
        fieldnames = list(unique_glyphs[0].keys())
        save_csv(unique_glyphs, csv_path, fieldnames)

    validation = validate_khitan(unique_glyphs, expected_count)
    save_json(validation, os.path.join(khitan_dir, "validation_results.json"))

    log_event("Khitan Large Script extraction complete", os.path.join(outdir, "extraction_log.txt"))
    return unique_glyphs
