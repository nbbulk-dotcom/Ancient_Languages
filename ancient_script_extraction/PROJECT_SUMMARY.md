# Ancient Script Glyph Extraction System – OCR Engine Implementation

This project implements a comprehensive OCR/Glyph Converter system for four ancient scripts—Linear A, Khitan Large Script, Proto-Elamite, and Indus Valley Script—using modular extraction pipelines and specialized image processing.

## Features

- **Modular Extractors**: Dedicated extraction modules for each ancient script
- **OCR Integration**: Specialized OCR subroutines for ancient script image processing
- **Glyph Databases**: Comprehensive JSON/CSV databases with metadata and validation
- **Image Processing**: CLAHE enhancement, adaptive thresholding, and morphological denoising
- **Validation Framework**: Completeness scoring and quality metrics
- **CI/CD Pipeline**: GitHub Actions workflow for automated extraction

## Architecture

### Data Sources
- **Linear A**: SigLA API and GORILA transcriptions
- **Khitan Large Script**: Unicode block U+18B00–U+18CFF and BabelStone database
- **Proto-Elamite**: CDLI API and tablet records
- **Indus Valley Script**: Harappa Archive and Mahadevan Concordance

### OCR Processing Pipeline
1. **Image Upload** → Ancient script photograph or scan
2. **Preprocessing** → CLAHE contrast enhancement and adaptive thresholding
3. **OCR Extraction** → Script-specific symbol recognition
4. **Symbol Conversion** → Glyph identification and normalization
5. **Database Storage** → JSON/CSV output with metadata

### Output Structure
```
output/
├── LinearA/
│   ├── LinearA_complete_glyphs.json
│   ├── LinearA_complete_glyphs.csv
│   ├── glyph_images/
│   └── validation_results.json
├── KhitanLargeScript/
├── ProtoElamite/
├── IndusValleyScript/
└── extraction_log.txt
```

## Usage

### Individual Script Extraction
```bash
cd ancient_script_extraction
python scripts/linear_a/extractor_linear_a.py --config config.yaml --outdir ./output
```

### All Scripts Extraction
```bash
cd ancient_script_extraction
python main.py
```

### OCR Image Processing
```python
from ocr_integration.glyph_ocr_processor import GlyphOCRProcessor

processor = GlyphOCRProcessor('./output')
result = processor.process_image(image_data, 'linear_a', 'sample.jpg')
```

## Validation Metrics

- **Linear A**: 87+ glyphs, 70%+ image coverage, SigLA primary source
- **Khitan**: 500+ glyphs, 80%+ Unicode coverage, Unicode primary source
- **Proto-Elamite**: 1000+ glyphs, 90%+ M-code coverage, CDLI primary source
- **Indus Valley**: 400+ glyphs, 50%+ H-code coverage, Harappa primary source

## License

© 2025 Nicolas Brett. All rights reserved.
Academic Research License - Free for non-commercial academic use.

## Integration

This OCR engine is designed to work independently from the MANUS frequency analysis system, providing raw glyph recognition and conversion capabilities for archaeological research and ancient script digitization projects.
