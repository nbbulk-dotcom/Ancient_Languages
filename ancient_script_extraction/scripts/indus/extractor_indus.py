import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.http_client import rate_limited_get, set_rate_limits
from utils.saver import save_json, save_csv, save_image
from utils.logger import log_event
from utils.dedupe import deduplicate_glyphs
from scripts.indus.indus_parsers import parse_harappa_archive, parse_mahadevan_concordance
from scripts.indus.validators import validate_indus

def run_indus_extraction(config, outdir):
    set_rate_limits(config.get('rate_limits', {}))
    harappa_url = config['sources']['IndusValleyScript'][0]['url']
    expected_count = config['expected_counts']['IndusValleyScript']
    
    indus_dir = os.path.join(outdir, "IndusValleyScript")
    os.makedirs(indus_dir, exist_ok=True)
    os.makedirs(os.path.join(indus_dir, "glyph_images"), exist_ok=True)

    log_event("Starting Indus Valley Script extraction", os.path.join(outdir, "extraction_log.txt"))

    parsed = []
    
    try:
        harappa_glyphs = parse_harappa_archive(harappa_url)
        parsed.extend(harappa_glyphs)
        log_event(f"Extracted {len(harappa_glyphs)} glyphs from Harappa Archive", os.path.join(outdir, "extraction_log.txt"))
    except Exception as e:
        log_event(f"Harappa Archive extraction failed: {str(e)}", os.path.join(outdir, "extraction_log.txt"))

    try:
        mahadevan_pdf = config['sources']['IndusValleyScript'][1].get('pdf')
        if mahadevan_pdf and os.path.exists(mahadevan_pdf):
            mahadevan_glyphs = parse_mahadevan_concordance(mahadevan_pdf)
            parsed.extend(mahadevan_glyphs)
            log_event(f"Extracted {len(mahadevan_glyphs)} glyphs from Mahadevan Concordance", os.path.join(outdir, "extraction_log.txt"))
    except Exception as e:
        log_event(f"Mahadevan Concordance extraction failed: {str(e)}", os.path.join(outdir, "extraction_log.txt"))

    unique_glyphs = deduplicate_glyphs(parsed)

    json_path = os.path.join(indus_dir, "IndusValleyScript_complete_glyphs.json")
    csv_path = os.path.join(indus_dir, "IndusValleyScript_complete_glyphs.csv")
    save_json(unique_glyphs, json_path)
    
    if unique_glyphs:
        fieldnames = list(unique_glyphs[0].keys())
        save_csv(unique_glyphs, csv_path, fieldnames)

    validation = validate_indus(unique_glyphs, expected_count)
    save_json(validation, os.path.join(indus_dir, "validation_results.json"))

    log_event("Indus Valley Script extraction complete", os.path.join(outdir, "extraction_log.txt"))
    return unique_glyphs
