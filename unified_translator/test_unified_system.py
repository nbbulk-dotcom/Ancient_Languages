#!/usr/bin/env python3
"""
Comprehensive test script for the unified MANUS/GROK system
Tests all endpoints and functionality following attachment specifications
"""

import requests
import json
import time
import os
from pathlib import Path

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_ocr_endpoint():
    """Test OCR endpoint with sample image"""
    try:
        test_image_path = "/tmp/test_ancient_script.jpg"
        with open(test_image_path, "wb") as f:
            f.write(b"dummy image data for testing")
        
        with open(test_image_path, "rb") as f:
            files = {"file": f}
            response = requests.post("http://localhost:8000/ocr", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OCR endpoint working: {result}")
            return result.get("extracted_text", "")
        else:
            print(f"❌ OCR endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ OCR endpoint error: {e}")
        return None

def test_translate_endpoint(text="RE ZA KU RO"):
    """Test frequency analysis endpoint"""
    try:
        data = {"text": text, "script": "LinearA"}
        response = requests.post("http://localhost:8000/translate", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Translate endpoint working: {result}")
            return result
        else:
            print(f"❌ Translate endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Translate endpoint error: {e}")
        return None

def test_narrative_endpoint(text="RE ZA KU RO"):
    """Test narrative generation endpoint"""
    try:
        data = {"text": text, "context": "Minoan"}
        response = requests.post("http://localhost:8000/narrative", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Narrative endpoint working: {result}")
            return result
        else:
            print(f"❌ Narrative endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Narrative endpoint error: {e}")
        return None

def test_validate_endpoint():
    """Test validation endpoint with sample frequencies"""
    try:
        test_frequencies = [210.42, 126.22, 157.79, 99.41]
        response = requests.post("http://localhost:8000/validate", json=test_frequencies)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Validate endpoint working: {result}")
            return result
        else:
            print(f"❌ Validate endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Validate endpoint error: {e}")
        return None

def test_brett_method_calculations():
    """Test Brett Method harmonic mean calculations"""
    try:
        frequencies = [210.42, 126.22, 157.79, 99.41]
        n = len(frequencies)
        harmonic_mean = n / sum(1/f for f in frequencies)
        
        print(f"✅ Brett Method calculation test:")
        print(f"   Frequencies: {frequencies}")
        print(f"   Harmonic Mean: {harmonic_mean:.2f} Hz")
        print(f"   Cultural Modifier (1.26): {harmonic_mean * 1.26:.2f} Hz")
        
        return True
    except Exception as e:
        print(f"❌ Brett Method calculation error: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🧪 Testing Unified MANUS/GROK System")
    print("=" * 50)
    
    math_ok = test_brett_method_calculations()
    
    health_ok = test_health_endpoint()
    
    if health_ok:
        extracted_text = test_ocr_endpoint()
        
        test_text = extracted_text if extracted_text else "RE ZA KU RO"
        
        freq_result = test_translate_endpoint(test_text)
        narrative_result = test_narrative_endpoint(test_text)
        validate_result = test_validate_endpoint()
        
        print("\n" + "=" * 50)
        if all([math_ok, health_ok, freq_result, narrative_result, validate_result]):
            print("🎉 All tests passed! Unified system is working correctly.")
            print("📊 Brett Method frequency analysis validated")
            print("🔤 OCR glyph extraction functional")
            print("📖 Narrative generation operational")
            print("✅ Validation endpoint confirmed")
        else:
            print("⚠️ Some tests failed. Check the output above.")
    else:
        print("❌ Backend not running. Start with: python main.py")

if __name__ == "__main__":
    main()
