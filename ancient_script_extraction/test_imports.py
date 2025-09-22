import sys
import os

try:
    import easyocr
    print("✓ EasyOCR imported successfully")
except ImportError as e:
    print(f"✗ EasyOCR import failed: {e}")

try:
    import imagehash
    from PIL import Image
    print("✓ imagehash and PIL imported successfully")
except ImportError as e:
    print(f"✗ imagehash/PIL import failed: {e}")

try:
    from ocr.ocr_pipeline import get_easyocr_reader, preprocess_for_ocr
    print("✓ OCR pipeline imports successful")
except ImportError as e:
    print(f"✗ OCR pipeline import failed: {e}")

try:
    from utils.logger import log_event
    from utils.http_client import safe_get
    from utils.saver import save_json
    print("✓ Enhanced utilities import successful")
except ImportError as e:
    print(f"✗ Enhanced utilities import failed: {e}")

print("Import test completed")
