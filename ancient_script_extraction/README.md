# Ancient Script Extraction (refined)

Purpose: Build reproducible glyph inventories and image sets for Linear A, Khitan Large Script, Proto-Elamite, Indus Valley Script. Includes robust OCR fallback, provenance, and statistical validation.

Quick start:
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. Edit config.yaml to add API keys and confirm endpoints
4. python main.py --config config.yaml --outdir ./output

Outputs: JSON/CSV per script, image directories, extraction_summary.json, validation_results.json, extraction_log.txt.
