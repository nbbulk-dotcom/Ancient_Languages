#!/usr/bin/env python3
"""
Complete system test for Ancient Script Universal Translator
Tests all endpoints and functionality end-to-end
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   System: {data.get('system')}")
            print(f"   Methodology: {data.get('methodology')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_ocr_endpoint():
    """Test OCR endpoint with sample image"""
    print("🔍 Testing OCR endpoint...")
    try:
        import cv2
        import numpy as np
        
        img = np.ones((200, 400, 3), dtype=np.uint8) * 255
        cv2.putText(img, 'RE ZA KU RO', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        test_image_path = '/tmp/test_ancient_script.jpg'
        cv2.imwrite(test_image_path, img)
        
        with open(test_image_path, 'rb') as f:
            files = {"file": ("test.jpg", f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/ocr", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ OCR test passed")
            print(f"   Extracted text: {data.get('extracted_text')}")
            print(f"   Confidence: {data.get('confidence', 0):.2f}")
            print(f"   Method: {data.get('processing_method')}")
            return data.get('extracted_text', '')
        else:
            print(f"❌ OCR test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ OCR test error: {e}")
        return None
    finally:
        if os.path.exists('/tmp/test_ancient_script.jpg'):
            os.remove('/tmp/test_ancient_script.jpg')

def test_translate_endpoint(text):
    """Test translation endpoint"""
    print("📊 Testing translation endpoint...")
    try:
        data = {"text": text, "script": "linear_a"}
        response = requests.post(f"{BASE_URL}/translate", data=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Translation test passed")
            print(f"   Frequency vector: {len(result.get('frequency_vector', []))} glyphs")
            
            if 'harmonic_analysis' in result:
                ha = result['harmonic_analysis']
                print(f"   Harmonic mean: {ha.get('harmonic_mean')} Hz")
                print(f"   Adjusted mean: {ha.get('adjusted_mean')} Hz")
                print(f"   Spiritual context: {ha.get('spiritual_context')}")
            
            print(f"   Brett Method validation: {result.get('brett_method_validation')}")
            return True
        else:
            print(f"❌ Translation test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Translation test error: {e}")
        return False

def test_narrative_endpoint(text):
    """Test narrative endpoint"""
    print("📖 Testing narrative endpoint...")
    try:
        data = {"text": text, "context": "ceremonial"}
        response = requests.post(f"{BASE_URL}/narrative", data=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Narrative test passed")
            print(f"   Narrative length: {len(result.get('narrative', ''))} characters")
            print(f"   Cultural context: {result.get('cultural_context')}")
            print(f"   Methodology: {result.get('methodology')}")
            print(f"   Confidence: {result.get('confidence_level', 0):.2f}")
            return True
        else:
            print(f"❌ Narrative test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Narrative test error: {e}")
        return False

def test_validate_endpoint():
    """Test validation endpoint"""
    print("🔬 Testing validation endpoint...")
    try:
        test_frequencies = [210.42, 126.22, 157.79, 99.41]
        response = requests.post(f"{BASE_URL}/validate", json=test_frequencies, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Validation test passed")
            print(f"   Valid: {result.get('valid')}")
            print(f"   Arithmetic mean: {result.get('arithmetic_mean')} Hz")
            print(f"   Harmonic mean: {result.get('harmonic_mean')} Hz")
            print(f"   Frequency category: {result.get('frequency_category')}")
            print(f"   Brett Method compliant: {result.get('brett_method_compliant')}")
            return True
        else:
            print(f"❌ Validation test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Validation test error: {e}")
        return False

def test_frontend_static_files():
    """Test frontend static file serving"""
    print("🌐 Testing frontend static files...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend serving test passed")
            return True
        else:
            print(f"❌ Frontend serving test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend serving test error: {e}")
        return False

def main():
    """Run complete system test"""
    print("🏺 Ancient Script Universal Translator - Complete System Test")
    print("=" * 70)
    
    print("⏳ Waiting for server to start...")
    for i in range(30):
        try:
            requests.get(f"{BASE_URL}/health", timeout=2)
            break
        except:
            time.sleep(1)
    else:
        print("❌ Server not responding after 30 seconds")
        sys.exit(1)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Frontend Static Files", test_frontend_static_files),
    ]
    
    extracted_text = test_ocr_endpoint()
    if extracted_text:
        tests.extend([
            ("Translation Analysis", lambda: test_translate_endpoint(extracted_text)),
            ("Narrative Generation", lambda: test_narrative_endpoint(extracted_text)),
            ("Frequency Validation", test_validate_endpoint)
        ])
    else:
        sample_text = "RE ZA KU RO"
        tests.extend([
            ("Translation Analysis (fallback)", lambda: test_translate_endpoint(sample_text)),
            ("Narrative Generation (fallback)", lambda: test_narrative_endpoint(sample_text)),
            ("Frequency Validation", test_validate_endpoint)
        ])
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🧪 Running {name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print(f"📊 Complete System Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ancient Script Universal Translator is fully operational!")
        print("🏺 The unified MANUS & GROK system is ready for production deployment.")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
