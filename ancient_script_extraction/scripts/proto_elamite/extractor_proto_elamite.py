import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.http_client import rate_limited_get, set_rate_limits, safe_get
from utils.saver import save_json, save_csv, save_image
from utils.logger import log_event
from utils.dedupe import deduplicate_glyphs
from scripts.proto_elamite.proto_elamite_parsers import parse_cdli_api
from scripts.proto_elamite.validators import validate_proto_elamite

def run_proto_elamite_extraction(config, outdir):
    set_rate_limits(config.get('rate_limits', {}))
    cdli_api = config['sources']['ProtoElamite'][0]['api']
    expected_count = config['expected_counts']['ProtoElamite']
    
    proto_elamite_dir = os.path.join(outdir, "ProtoElamite")
    os.makedirs(proto_elamite_dir, exist_ok=True)
    os.makedirs(os.path.join(proto_elamite_dir, "glyph_images"), exist_ok=True)

    log_event("Starting Proto-Elamite extraction", os.path.join(outdir, "extraction_log.txt"))

    parsed = []
    
    try:
        response = rate_limited_get(cdli_api + "tablets?period=proto-elamite")
        tablets = response.json()
        parsed = parse_cdli_api(tablets)
        log_event(f"Extracted {len(parsed)} glyphs from CDLI API", os.path.join(outdir, "extraction_log.txt"))
    except Exception as e:
        log_event(f"CDLI API extraction failed: {str(e)}", os.path.join(outdir, "extraction_log.txt"))

    unique_glyphs = deduplicate_glyphs(parsed)

    json_path = os.path.join(proto_elamite_dir, "ProtoElamite_complete_glyphs.json")
    csv_path = os.path.join(proto_elamite_dir, "ProtoElamite_complete_glyphs.csv")
    save_json(unique_glyphs, json_path)
    
    if unique_glyphs:
        fieldnames = list(unique_glyphs[0].keys())
        save_csv(unique_glyphs, csv_path, fieldnames)

    validation = validate_proto_elamite(unique_glyphs, expected_count)
    save_json(validation, os.path.join(proto_elamite_dir, "validation_results.json"))

    log_event("Proto-Elamite extraction complete", os.path.join(outdir, "extraction_log.txt"))
    return unique_glyphs
