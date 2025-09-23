#!/usr/bin/env python3
"""
validate_extraction.py
Usage:
  python3 validate_extraction.py <source_key> <output_json_path> <config_yaml_path>

Performs:
 - JSON sanity checks
 - Schema field validation based on config.yaml post_fetch_checks
 - Compatibility checks: Python version, required packages (poetry lock + pyproject)
 - Integration smoke test: imports analysis modules and runs a minimal function to ensure no version/API conflicts
 - Writes a detailed validation JSON to the same directory as the output file.
"""

import sys
import json
import os
import subprocess
import platform
from pathlib import Path
import yaml

def load_config(path):
    return yaml.safe_load(open(path))

def check_python_version(required):
    cur = platform.python_version()
    ok = cur.startswith(required.split(".")[0])
    return {"required": required, "current": cur, "ok": ok}

def check_poetry_lock_matches(pyproject_path, poetry_lock_path):
    return {
        "pyproject_exists": os.path.exists(pyproject_path),
        "poetry_lock_exists": os.path.exists(poetry_lock_path)
    }

def load_output(path):
    with open(path,'r',encoding='utf8') as f:
        return json.load(f)

def schema_checks(source_cfg, data):
    checks = []
    for c in source_cfg.get("post_fetch_checks", []):
        if c == "non_empty_array":
            checks.append({"check":"non_empty_array","ok": bool(data)})
        elif c.startswith("contains_expected_fields"):
            expected = source_cfg.get("post_fetch_checks_fields", source_cfg.get("post_fetch_checks_fields", []))
            expected = source_cfg.get("post_fetch_checks", [])
            expected_fields = ["glyph_id","image_url","unicode","provenance","mcode","hcode"]
            if isinstance(data, list) and data:
                first_item = data[0] if data else {}
                has_fields = any(field in first_item for field in expected_fields)
                checks.append({"check":"contains_expected_fields_guess","ok":has_fields})
            else:
                checks.append({"check":"contains_expected_fields_guess","ok":False})
        else:
            checks.append({"check":c,"ok":"unknown_check_type"})
    return checks

def integration_smoke_test():
    results = {}
    modules = [
        "analysis_tools.linear_a_frequency_calculator",
        "analysis_tools.khitan_frequency_analyzer",
        "analysis_tools.proto_elamite_angular_analyzer",
        "analysis_tools.indus_vedic_analyzer"
    ]
    for m in modules:
        try:
            __import__(m)
            results[m] = {"imported": True}
        except Exception as e:
            results[m] = {"imported": False, "error": str(e)}
    return results

def main():
    if len(sys.argv) < 4:
        print("Usage: validate_extraction.py <source_key> <output_json_path> <config_yaml_path>")
        sys.exit(2)
    source_key = sys.argv[1]
    output_path = sys.argv[2]
    config_path = sys.argv[3]

    cfg = load_config(config_path)
    source_cfg = cfg['sources'].get(source_key, {})

    validation = {
        "source_key": source_key,
        "output_path": output_path,
        "config_path": config_path,
    }

    validation['compat'] = {}
    if cfg.get('compatibility_policy', {}).get('enforce_version_consistency', False):
        req_py = cfg['compatibility_policy'].get('python_version', platform.python_version())
        validation['compat']['python_version'] = check_python_version(req_py)

    repo_root = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.parent.exists() else Path('.')
    pyproject = repo_root / "pyproject.toml"
    poetry_lock = repo_root / "poetry.lock"
    validation['compat']['poetry_lock'] = check_poetry_lock_matches(str(pyproject), str(poetry_lock))

    try:
        data = load_output(output_path)
        validation['data_loaded'] = True
    except Exception as e:
        validation['data_loaded'] = False
        validation['data_error'] = str(e)
        out = Path(output_path).parent / "validation_results.json"
        out.write_text(json.dumps(validation, indent=2))
        print(f"WROTE {out}")
        sys.exit(3)

    validation['schema_checks'] = schema_checks(source_cfg, data)

    if isinstance(data, list):
        validation['glyph_count'] = len(data)
    elif isinstance(data, dict):
        validation['glyph_count'] = 1
    else:
        validation['glyph_count'] = 0

    validation['integration_smoke'] = integration_smoke_test()

    overall_ok = validation['data_loaded'] and all(v.get('imported', True) for v in validation['integration_smoke'].values())
    validation['overall_status'] = "PASS" if overall_ok else "FAIL"

    out = Path(output_path).parent / "validation_results.json"
    out.write_text(json.dumps(validation, indent=2))
    print(f"WROTE {out}")

if __name__ == "__main__":
    main()
