#!/usr/bin/env python3

import pytesseract
from PIL import Image
import io

def test_ocr():
    """Test if tesseract is working locally"""
    try:
        print('Testing tesseract installation...')
        result = pytesseract.get_tesseract_version()
        print(f'Tesseract version: {result}')
        
        image = Image.open('/home/ubuntu/attachments/1923494e-9de9-4b39-bf73-1e5098ad8f68/image.png')
        processed = image.convert('L')
        extracted_text = pytesseract.image_to_string(processed, config='--psm 6')
        print(f'Extracted text: "{extracted_text.strip()}"')
        print('Local OCR test successful!')
        
    except Exception as e:
        print(f'OCR test failed: {e}')

if __name__ == "__main__":
    test_ocr()
