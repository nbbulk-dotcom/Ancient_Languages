# Ancient Script Glyph Extraction System

This repository implements a modular pipeline for extracting, validating, and packaging glyph inventories from four undeciphered ancient scripts:

- Linear A
- Khitan Large Script
- Proto-Elamite
- Indus Valley Script

## Purpose

To support the Brett Method of frequency-based analysis and symbolic resonance mapping, this system builds complete glyph databases with image sets, metadata, and validation outputs.

## Features

- Modular extractors per script
- Image normalization and deduplication
- Frequency analysis and context mapping
- JSON/CSV output formats
- CI-ready GitHub Actions workflow
- Validation and completeness scoring
- Optional font generation (Khitan)

## Getting Started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/linear_a/extractor_linear_a.py --config config.yaml --outdir ./output
```

## Output Structure
```
output/
├── LinearA_complete_glyphs.json
├── LinearA_complete_glyphs.csv
├── LinearA_glyph_images/
├── extraction_summary.json
├── validation_results.json
├── extraction_log.txt
```

## License

© 2025 Nicolas Brett. All rights reserved.
Academic Research License - Free for non-commercial academic use.
