import os
import sys
import json
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.http_client import rate_limited_get, set_rate_limits
from utils.saver import save_json, save_csv, save_image
from utils.logger import log_event
from utils.dedupe import deduplicate_glyphs
from scripts.linear_a.linear_a_parsers import parse_sigla_api
from scripts.linear_a.linear_a_image_downloader import download_linear_a_images
from scripts.linear_a.validators import validate_linear_a

def run_linear_a_extraction(config, outdir):
    set_rate_limits(config.get('rate_limits', {}))
    sigla_api = config['sources']['LinearA'][0]['api']
    expected_count = config['expected_counts']['LinearA']
    
    linear_a_dir = os.path.join(outdir, "LinearA")
    os.makedirs(linear_a_dir, exist_ok=True)
    os.makedirs(os.path.join(linear_a_dir, "glyph_images"), exist_ok=True)

    log_event("Starting Linear A extraction", os.path.join(outdir, "extraction_log.txt"))

    try:
        response = rate_limited_get(sigla_api + "signs")
        signs = response.json()
    except Exception as e:
        log_event(f"Failed to fetch from SigLA API: {str(e)}", os.path.join(outdir, "extraction_log.txt"))
        signs = []

    parsed = parse_sigla_api(signs)

    for glyph in parsed:
        if glyph.get("image_url"):
            img_path = os.path.join(linear_a_dir, "glyph_images", f"{glyph['sign_id']}.png")
            try:
                image_bytes = download_linear_a_images(glyph["image_url"])
                save_image(image_bytes, img_path)
                glyph["character_image"] = img_path
            except Exception as e:
                log_event(f"Image download failed for {glyph['sign_id']}: {str(e)}", os.path.join(outdir, "extraction_log.txt"))
                glyph["character_image"] = None

    unique_glyphs = deduplicate_glyphs(parsed)

    json_path = os.path.join(linear_a_dir, "LinearA_complete_glyphs.json")
    csv_path = os.path.join(linear_a_dir, "LinearA_complete_glyphs.csv")
    save_json(unique_glyphs, json_path)
    
    if unique_glyphs:
        fieldnames = list(unique_glyphs[0].keys())
        save_csv(unique_glyphs, csv_path, fieldnames)

    validation = validate_linear_a(unique_glyphs, expected_count)
    save_json(validation, os.path.join(linear_a_dir, "validation_results.json"))

    log_event("Linear A extraction complete", os.path.join(outdir, "extraction_log.txt"))
    return unique_glyphs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract Linear A glyphs')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--outdir', default='./output', help='Output directory')
    args = parser.parse_args()
    
    import yaml
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    run_linear_a_extraction(config, args.outdir)
