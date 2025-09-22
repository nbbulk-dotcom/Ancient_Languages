#!/usr/bin/env python3
"""
Comprehensive test runner for Ancient Script Universal Translator
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🧪 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def test_python_imports():
    """Test Python imports"""
    imports = [
        "import fastapi",
        "import uvicorn", 
        "import cv2",
        "import pytesseract",
        "import easyocr",
        "import numpy",
        "import PIL"
    ]
    
    for imp in imports:
        if not run_command(f"python -c '{imp}'", f"Import test: {imp}"):
            return False
    return True

def test_ocr_functionality():
    """Test OCR functionality"""
    test_script = """
import cv2
import numpy as np
import pytesseract
from ocr_linear_a_subroutine import ocr_linear_a_subroutine

img = np.ones((100, 200, 3), dtype=np.uint8) * 255
cv2.putText(img, 'TEST', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.imwrite('/tmp/test_ocr.jpg', img)

result, confidence = ocr_linear_a_subroutine('/tmp/test_ocr.jpg')
print(f"OCR Result: {result}, Confidence: {confidence}")
"""
    
    return run_command(f"python -c \"{test_script}\"", "OCR functionality test")

def test_docker_build():
    """Test Docker build"""
    return run_command("docker build -t ancient-translator-test .", "Docker build test")

def test_api_endpoints():
    """Test API endpoints"""
    print("🧪 Testing API endpoints...")
    
    server_process = subprocess.Popen([
        "python", "-c", 
        "import uvicorn; uvicorn.run('main:app', host='127.0.0.1', port=8001, log_level='error')"
    ])
    
    time.sleep(10)
    
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code != 200:
            print("❌ Health endpoint failed")
            return False
        
        print("✅ API endpoints test passed")
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False
    finally:
        server_process.terminate()
        server_process.wait()

def main():
    """Run all tests"""
    print("🏺 Ancient Script Universal Translator - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Python imports", test_python_imports),
        ("OCR functionality", test_ocr_functionality),
        ("Docker build", test_docker_build),
        ("API endpoints", test_api_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Please fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
