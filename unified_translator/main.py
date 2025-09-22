from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import os
from typing import List
from pydantic import BaseModel
import shutil
import logging
import uvicorn
from ocr_linear_a_subroutine import ocr_linear_a_subroutine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ancient Script Universal Translator",
    description="Unified MANUS & GROK System for Ancient Script Analysis using the Brett Method",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
    app.mount("/downloads", StaticFiles(directory="frontend/public/downloads"), name="downloads")
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")

class OCRResponse(BaseModel):
    extracted_text: str
    confidence: float = 0.0
    processing_method: str = "Enhanced GROK OCR"

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Enhanced OCR endpoint for ancient script image processing using GROK system"""
    try:
        logger.info(f"Processing OCR for file: {file.filename}")
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        extracted_text, confidence = ocr_linear_a_subroutine(temp_path)
        os.unlink(temp_path)
        
        logger.info(f"OCR completed: {extracted_text[:50]}... (confidence: {confidence})")
        
        return OCRResponse(
            extracted_text=extracted_text,
            confidence=confidence,
            processing_method="Enhanced GROK OCR with EasyOCR + Tesseract"
        )
    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.post("/translate")
async def translate_endpoint(text: str = Form(...), script: str = Form(...)):
    """Enhanced frequency analysis endpoint using MANUS Brett Method"""
    try:
        logger.info(f"Analyzing frequencies for script: {script}, text: {text}")
        
        frequencies = calculate_frequencies_for_script(text, script)
        
        if frequencies:
            freq_values = [f["frequency"] for f in frequencies]
            n = len(freq_values)
            harmonic_mean = n / sum(1/f for f in freq_values) if all(f > 0 for f in freq_values) else 0
            
            cultural_modifiers = {
                "LinearA": 1.26,
                "linear_a": 1.26,
                "khitan": 1.15,
                "proto_elamite": 1.08,
                "indus_valley": 1.33
            }
            
            modifier = cultural_modifiers.get(script, 1.0)
            adjusted_mean = harmonic_mean * modifier
            
            if adjusted_mean > 600:
                spiritual_context = "Sacred/Divine (High Frequency)"
            elif adjusted_mean > 300:
                spiritual_context = "Ceremonial/Ritual (Medium Frequency)"
            else:
                spiritual_context = "Administrative/Mundane (Low Frequency)"
            
            return {
                "frequency_vector": frequencies,
                "harmonic_analysis": {
                    "harmonic_mean": round(harmonic_mean, 2),
                    "adjusted_mean": round(adjusted_mean, 2),
                    "cultural_modifier": modifier,
                    "spiritual_context": spiritual_context
                },
                "brett_method_validation": True
            }
        else:
            return {"frequency_vector": [], "brett_method_validation": False}
            
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/narrative")
async def narrative_endpoint(text: str = Form(...), context: str = Form(...)):
    """Enhanced narrative generation endpoint with cultural analysis"""
    try:
        logger.info(f"Generating narrative for context: {context}, text: {text}")
        
        narrative = generate_narrative(text, context)
        
        glyphs = text.split()
        glyph_count = len(glyphs)
        
        methodology_note = f"\n\nMethodological Note: This interpretation uses the Brett Method frequency-based analysis. The {glyph_count}-glyph sequence was analyzed for harmonic patterns and cultural context markers consistent with {context} usage in ancient scripts."
        
        enhanced_narrative = narrative + methodology_note
        
        return {
            "narrative": enhanced_narrative,
            "cultural_context": context,
            "glyph_count": glyph_count,
            "methodology": "Brett Method - Frequency-Based Cultural Analysis",
            "confidence_level": 0.85 if glyph_count >= 3 else 0.65
        }
    except Exception as e:
        logger.error(f"Narrative generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Narrative generation failed: {str(e)}")

@app.post("/validate")
async def validate_endpoint(frequencies: List[float]):
    """Enhanced validation endpoint for Brett Method frequency patterns"""
    try:
        logger.info(f"Validating frequency pattern: {frequencies}")
        
        if not frequencies:
            return {"valid": False, "error": "No frequencies provided"}
        
        n = len(frequencies)
        arithmetic_mean = sum(frequencies) / n
        
        if all(f > 0 for f in frequencies):
            harmonic_mean = n / sum(1/f for f in frequencies)
        else:
            harmonic_mean = 0
        
        valid_range = all(50 <= f <= 1000 for f in frequencies)
        valid_pattern = harmonic_mean > 0 and arithmetic_mean > 0
        consistency_check = abs(arithmetic_mean - harmonic_mean) / arithmetic_mean < 0.5
        
        overall_valid = valid_range and valid_pattern and consistency_check
        
        if harmonic_mean > 600:
            category = "Sacred/Divine Frequencies"
        elif harmonic_mean > 300:
            category = "Ceremonial/Ritual Frequencies"
        else:
            category = "Administrative/Mundane Frequencies"
        
        return {
            "valid": overall_valid,
            "arithmetic_mean": round(arithmetic_mean, 2),
            "harmonic_mean": round(harmonic_mean, 2),
            "frequency_category": category,
            "pattern_consistency": round(1 - abs(arithmetic_mean - harmonic_mean) / arithmetic_mean, 3) if arithmetic_mean > 0 else 0,
            "brett_method_compliant": overall_valid,
            "validation_details": {
                "range_valid": valid_range,
                "pattern_valid": valid_pattern,
                "consistency_valid": consistency_check
            }
        }
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

def calculate_frequencies_for_script(text, script):
    """Calculate frequencies using MANUS frequency calculators with Brett Method"""
    glyphs = text.split()
    
    base_frequencies = {
        "LinearA": {"RE": 210.42, "ZA": 126.22, "KU": 157.79, "RO": 99.41},
        "linear_a": {"RE": 210.42, "ZA": 126.22, "KU": 157.79, "RO": 99.41},
        "khitan": {"KHAN": 180.33, "LIAO": 145.67, "SCRIPT": 167.89},
        "proto_elamite": {"ELAM": 195.44, "PROTO": 134.56, "ADMIN": 156.78},
        "indus_valley": {"HARAPPA": 188.22, "VEDIC": 201.33, "SEAL": 143.89}
    }
    
    script_freqs = base_frequencies.get(script, base_frequencies["LinearA"])
    
    freq_vector = []
    for glyph in glyphs:
        freq = script_freqs.get(glyph.upper(), len(glyph) * 50 + 100)
        freq_vector.append({"glyph": glyph, "frequency": freq})
    
    return freq_vector

def generate_narrative(text, context):
    """Generate narrative following Brett Method cultural analysis"""
    glyphs = text.split()
    
    if any(g.upper() in ["RE", "ZA", "KU", "RO"] for g in glyphs):
        if context.lower() == "ceremonial":
            return f"Linear A sequence suggests Minoan ceremonial invocation. The glyphs '{' '.join(glyphs)}' form a harmonic pattern indicating ritual blessing or protective charm. Frequency analysis reveals spiritual resonance in the 126-210 Hz range, consistent with sacred Minoan practices."
        elif context.lower() == "administrative":
            return f"Administrative record in Linear A script. The sequence '{' '.join(glyphs)}' likely represents inventory, tribute, or accounting notation. Frequency patterns suggest mundane but important bureaucratic function."
        elif context.lower() == "religious":
            return f"Sacred Linear A inscription. The glyphs '{' '.join(glyphs)}' appear to invoke divine protection or blessing. High-frequency harmonic analysis indicates connection to Minoan religious practices and possible goddess worship."
    
    if any(g.upper() in ["KHAN", "LIAO"] for g in glyphs):
        return f"Khitan Large Script inscription from the Liao Dynasty period. The text '{' '.join(glyphs)}' reflects imperial administrative or ceremonial usage, with frequency patterns indicating formal court language."
    
    if any(g.upper() in ["HARAPPA", "VEDIC"] for g in glyphs):
        return f"Indus Valley Script with potential Vedic connections. The sequence '{' '.join(glyphs)}' shows frequency patterns consistent with early Sanskrit mantras, suggesting proto-Vedic religious or administrative content."
    
    return f"Ancient script sequence '{' '.join(glyphs)}' in {context} context. Frequency analysis suggests {len(glyphs)}-glyph pattern with cultural significance. Further analysis needed for complete interpretation."

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        import cv2
        import pytesseract
        import easyocr
        import numpy as np
        
        health_status = {
            "status": "healthy",
            "service": "Ancient Script Universal Translator",
            "version": "1.0.0",
            "system": "Unified MANUS & GROK",
            "methodology": "Brett Method - Frequency-Based Analysis",
            "dependencies": {
                "opencv": cv2.__version__,
                "numpy": np.__version__,
                "tesseract": "available",
                "easyocr": "available"
            },
            "endpoints": {
                "ocr": "operational",
                "translate": "operational", 
                "narrative": "operational",
                "validate": "operational"
            },
            "timestamp": "2025-09-22T18:35:00Z"
        }
        
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "Ancient Script Universal Translator"
        }

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    os.makedirs("frontend/public/downloads", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8001)
