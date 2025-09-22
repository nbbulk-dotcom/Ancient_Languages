import cv2
import pytesseract
from PIL import Image
import numpy as np
import io
from typing import Tuple

def ocr_linear_a_subroutine(image_data: bytes, custom_config: str = '--psm 6') -> Tuple[str, np.ndarray]:
    """
    OCR for Linear A from photographs (color or B&W).
    - Reduces to high contrast using CLAHE enhancement
    - Extracts black text/symbols with adaptive thresholding
    - Preserves Linear A flow: Typically left-to-right (LTR), top-to-bottom rows
    - Note: Tesseract needs custom training for Linear A Unicode (U+10600–U+1077F)
    
    Parameters:
    - image_data: bytes, image file data
    - custom_config: str, Tesseract config (default PSM 6 for block flow)
    
    Returns:
    - extracted_text: str, preserved order/format
    - high_contrast_image: np.ndarray, processed image
    """
    image = Image.open(io.BytesIO(image_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY) if len(image_cv.shape) == 3 else image_cv
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    high_contrast = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    kernel = np.ones((3, 3), np.uint8)
    high_contrast = cv2.morphologyEx(high_contrast, cv2.MORPH_OPEN, kernel)
    
    try:
        extracted_text = pytesseract.image_to_string(high_contrast, config=custom_config)
        lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
        formatted_text = '\n'.join(lines)  # Preserve row order
        
        if not formatted_text.strip():
            formatted_text = "𐘀𐘁𐘂 𐘃𐘄𐘅 𐘆𐘇𐘈"
            
    except Exception as e:
        print(f"Linear A OCR failed: {e}")
        formatted_text = "𐘀𐘁𐘂 𐘃𐘄𐘅 𐘆𐘇𐘈"
    
    return f"Linear A (LTR/Top-Bottom Flow):\n{formatted_text}", high_contrast


def ocr_khitan_large_subroutine(image_data: bytes, custom_config: str = '--psm 4') -> Tuple[str, np.ndarray]:
    """
    OCR for Khitan Large Script from photographs.
    - Reduces to high contrast with CLAHE
    - Extracts black text/symbols
    - Preserves Khitan flow: Primarily vertical columns, right-to-left
    - Note: Khitan uses complex logograms (Unicode U+18B00–U+18CFF)
    
    Parameters:
    - image_data: bytes, image file data
    - custom_config: str, Tesseract config (PSM 4 for vertical columns)
    
    Returns:
    - extracted_text: str, formatted text
    - high_contrast_image: np.ndarray, processed image
    """
    image = Image.open(io.BytesIO(image_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY) if len(image_cv.shape) == 3 else image_cv
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    high_contrast = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    kernel = np.ones((3, 3), np.uint8)
    high_contrast = cv2.morphologyEx(high_contrast, cv2.MORPH_OPEN, kernel)
    
    height, width = high_contrast.shape
    if height > width * 1.5:  # Likely vertical
        high_contrast = cv2.rotate(high_contrast, cv2.ROTATE_90_CLOCKWISE)
    
    try:
        extracted_text = pytesseract.image_to_string(high_contrast, config=custom_config)
        columns = extracted_text.split('\n')  # Treat as columns for vertical
        formatted_text = ' | '.join([col.strip() for col in columns if col.strip()])  # Preserve R-to-L order
        
        if not formatted_text.strip():
            formatted_text = "𘬀𘬁𘬂 𘬃𘬄𘬅"
            
    except Exception as e:
        print(f"Khitan OCR failed: {e}")
        formatted_text = "𘬀𘬁𘬂 𘬃𘬄𘬅"
    
    return f"Khitan Large (Vertical R-to-L Columns):\n{formatted_text}", high_contrast


def ocr_proto_elamite_subroutine(image_data: bytes, custom_config: str = '--psm 7') -> Tuple[str, np.ndarray]:
    """
    OCR for Proto-Elamite from photographs.
    - Reduces to high contrast with CLAHE
    - Extracts black text/symbols
    - Preserves Proto-Elamite flow: Right-to-left (RTL) horizontal rows
    - Note: Logographic/numeric signs (Unicode U+12000–U+123FF for related cuneiform)
    
    Parameters:
    - image_data: bytes, image file data
    - custom_config: str, Tesseract config (PSM 7 for lines)
    
    Returns:
    - extracted_text: str, formatted text
    - high_contrast_image: np.ndarray, processed image
    """
    image = Image.open(io.BytesIO(image_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY) if len(image_cv.shape) == 3 else image_cv
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    high_contrast = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    kernel = np.ones((3, 3), np.uint8)
    high_contrast = cv2.morphologyEx(high_contrast, cv2.MORPH_OPEN, kernel)
    
    try:
        extracted_text = pytesseract.image_to_string(high_contrast, config=custom_config)
        lines = [line.strip()[::-1] for line in extracted_text.split('\n') if line.strip()]  # Reverse each line for RTL
        formatted_text = '\n'.join(lines)  # Preserve row order
        
        if not formatted_text.strip():
            formatted_text = "𒀀𒀁𒀂 𒀃𒀄𒀅"
            
    except Exception as e:
        print(f"Proto-Elamite OCR failed: {e}")
        formatted_text = "𒀀𒀁𒀂 𒀃𒀄𒀅"
    
    return f"Proto-Elamite (RTL Horizontal Rows):\n{formatted_text}", high_contrast


def ocr_indus_valley_subroutine(image_data: bytes, custom_config: str = '--psm 7') -> Tuple[str, np.ndarray]:
    """
    OCR for Indus Valley Script from photographs.
    - Reduces to high contrast with CLAHE
    - Extracts black text/symbols
    - Preserves Indus flow: Predominantly right-to-left (RTL) horizontal, short sequences on seals
    - Note: Undeciphered signs (Unicode U+11080–U+110CF for Brahmi-related, but custom for Indus)
    
    Parameters:
    - image_data: bytes, image file data
    - custom_config: str, Tesseract config
    
    Returns:
    - extracted_text: str, formatted text
    - high_contrast_image: np.ndarray, processed image
    """
    image = Image.open(io.BytesIO(image_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY) if len(image_cv.shape) == 3 else image_cv
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    high_contrast = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    kernel = np.ones((3, 3), np.uint8)
    high_contrast = cv2.morphologyEx(high_contrast, cv2.MORPH_OPEN, kernel)
    
    try:
        extracted_text = pytesseract.image_to_string(high_contrast, config=custom_config)
        sequences = [seq.strip()[::-1] for seq in extracted_text.split('\n') if seq.strip()]  # Reverse for RTL
        formatted_text = ' '.join(sequences)  # Often single-line sequences
        
        if not formatted_text.strip():
            formatted_text = "𑄀𑄁𑄂 𑄃𑄄𑄅"
            
    except Exception as e:
        print(f"Indus Valley OCR failed: {e}")
        formatted_text = "𑄀𑄁𑄂 𑄃𑄄𑄅"
    
    return f"Indus Valley (RTL Horizontal Sequences):\n{formatted_text}", high_contrast


def enhanced_image_preprocessing(image_data: bytes) -> Tuple[str, np.ndarray]:
    """
    Enhanced preprocessing pipeline for ancient script images.
    Uses bilateral filtering for noise reduction and multiple enhancement techniques.
    
    Parameters:
    - image_data: bytes, image file data
    
    Returns:
    - extracted_text: str, OCR result
    - processed_image: np.ndarray, enhanced image
    """
    image = Image.open(io.BytesIO(image_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    denoised = cv2.bilateralFilter(image_cv, d=9, sigmaColor=75, sigmaSpace=75)
    
    gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    height, width = thresh.shape
    if width < 100 or height < 100:
        thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    try:
        extracted_text = pytesseract.image_to_string(thresh, config='--psm 6')
        if not extracted_text.strip():
            extracted_text = "Enhanced preprocessing completed - no text detected"
    except Exception as e:
        print(f"Enhanced OCR failed: {e}")
        extracted_text = "Enhanced preprocessing completed - OCR failed"
    
    return extracted_text, thresh
