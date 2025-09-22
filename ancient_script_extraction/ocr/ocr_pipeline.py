try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

from PIL import Image
import numpy as np

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.logger import log_event

_reader = None

def get_easyocr_reader(langs=None):
    global _reader
    if not EASYOCR_AVAILABLE:
        log_event("EasyOCR not available", level="WARNING")
        return None
    if _reader is None:
        try:
            langs = langs or ['en']
            _reader = easyocr.Reader(langs, gpu=False)
        except Exception as e:
            log_event(f"Failed to initialize EasyOCR: {e}", level="ERROR")
            return None
    return _reader

def preprocess_for_ocr(pil_image):
    """Preprocess image for better OCR results"""
    if not CV2_AVAILABLE:
        log_event("OpenCV not available, returning original image", level="WARNING")
        return pil_image
    
    try:
        img = np.array(pil_image.convert("RGB"))[:, :, ::-1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    except Exception as e:
        log_event(f"Image preprocessing failed: {e}", level="ERROR")
        return pil_image

def extract_text_easyocr(image_path_or_pil, langs=None):
    """Extract text using EasyOCR"""
    if not EASYOCR_AVAILABLE:
        log_event("EasyOCR not available", level="WARNING")
        return []
    
    try:
        reader = get_easyocr_reader(langs)
        if reader is None:
            return []
            
        if isinstance(image_path_or_pil, (str, Path)):
            result = reader.readtext(str(image_path_or_pil))
        else:
            preprocessed = preprocess_for_ocr(image_path_or_pil)
            if CV2_AVAILABLE:
                result = reader.readtext(preprocessed)
            else:
                img_array = np.array(image_path_or_pil)
                result = reader.readtext(img_array)
        
        text_results = []
        for (bbox, text, confidence) in result:
            if confidence > 0.5:
                text_results.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
        
        log_event(f"EasyOCR extracted {len(text_results)} text regions")
        return text_results
        
    except Exception as e:
        log_event(f"EasyOCR extraction failed: {e}", level="ERROR")
        return []

def extract_text_tesseract(image_path_or_pil):
    """Extract text using Tesseract OCR"""
    if not TESSERACT_AVAILABLE:
        log_event("Tesseract not available", level="WARNING")
        return []
    
    try:
        if isinstance(image_path_or_pil, (str, Path)):
            img = Image.open(image_path_or_pil)
        else:
            img = image_path_or_pil
        
        if CV2_AVAILABLE:
            preprocessed = preprocess_for_ocr(img)
            pil_preprocessed = Image.fromarray(preprocessed)
        else:
            pil_preprocessed = img
        
        text = pytesseract.image_to_string(pil_preprocessed)
        data = pytesseract.image_to_data(pil_preprocessed, output_type=pytesseract.Output.DICT)
        
        text_results = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 50 and data['text'][i].strip():
                text_results.append({
                    'text': data['text'][i],
                    'confidence': int(data['conf'][i]) / 100.0,
                    'bbox': [data['left'][i], data['top'][i], 
                            data['left'][i] + data['width'][i], 
                            data['top'][i] + data['height'][i]]
                })
        
        log_event(f"Tesseract extracted {len(text_results)} text regions")
        return text_results
        
    except Exception as e:
        log_event(f"Tesseract extraction failed: {e}", level="ERROR")
        return []

def extract_glyphs_from_image(image_path_or_pil, prefer_engine="easyocr", langs=None):
    """
    Extract glyphs/symbols from ancient script images using OCR
    """
    try:
        if prefer_engine == "easyocr" and EASYOCR_AVAILABLE:
            results = extract_text_easyocr(image_path_or_pil, langs)
            if results:
                return results
            log_event("EasyOCR failed, falling back to Tesseract")
            
        if TESSERACT_AVAILABLE:
            results = extract_text_tesseract(image_path_or_pil)
            if results:
                return results
        
        if prefer_engine != "easyocr" and EASYOCR_AVAILABLE:
            log_event("Tesseract failed, falling back to EasyOCR")
            results = extract_text_easyocr(image_path_or_pil, langs)
            if results:
                return results
        
        log_event("No OCR engines available or all failed", level="ERROR")
        return []
            
    except Exception as e:
        log_event(f"Glyph extraction failed: {e}", level="ERROR")
        return []

def get_available_engines():
    """Return list of available OCR engines"""
    engines = []
    if EASYOCR_AVAILABLE:
        engines.append("easyocr")
    if TESSERACT_AVAILABLE:
        engines.append("tesseract")
    return engines
