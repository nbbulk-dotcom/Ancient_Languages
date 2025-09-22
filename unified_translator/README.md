# Ancient Script Universal Translator - Unified System

This unified deployment system integrates the MANUS frequency analysis system with the GROK OCR engine, following The Brett Method for ancient script translation.

## Architecture

- **GROK System**: Handles OCR processing and glyph extraction from images
- **MANUS System**: Provides frequency analysis and cultural interpretation
- **Unified API**: FastAPI backend with endpoints: `/ocr`, `/translate`, `/narrative`, `/validate`
- **React Frontend**: "Convert Image to Characters" interface with frequency breakdown display

## Quick Start

```bash
# Deploy the unified system
chmod +x deploy.sh
./deploy.sh

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## API Endpoints

### POST /ocr
Extract glyphs from uploaded ancient script image using GROK OCR system.

### POST /translate
Convert extracted text to frequency analysis using MANUS frequency calculators.

### POST /narrative
Generate cultural narrative interpretation from frequency analysis.

### POST /validate
Validate frequency analysis using Brett Method mathematical principles.

## System Integration

The unified system connects:
1. Image upload → GROK OCR processing → glyph extraction
2. Extracted glyphs → MANUS frequency analysis → harmonic calculations
3. Frequency data → narrative generation → cultural interpretation
4. All results displayed in React frontend with step-by-step explanations

## Supported Scripts

- Linear A (Minoan civilization)
- Khitan Large Script (Liao dynasty)
- Proto-Elamite (ancient Iran)
- Indus Valley Script (Harappan civilization)

## The Brett Method

This system implements The Brett Method for frequency-based ancient script analysis:
- Harmonic mean calculations: `n / Σ(1/f_i)`
- Cultural context modifiers for different civilizations
- Spiritual/ceremonial frequency pattern recognition
- Multi-language narrative output

## Development

```bash
# Backend development
cd unified_translator
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm start
```

## Docker Deployment

The system uses Docker Compose for full-stack deployment:
- Backend: FastAPI with OCR and frequency analysis
- Frontend: React application
- Redis: Caching layer for performance
- Volume mounts: Integration with MANUS and GROK systems
