#!/usr/bin/env python3
"""
Health check script for Ancient Script Universal Translator
Tests all system components and endpoints
"""

import requests
import sys
import time
import json

def check_health_endpoint():
    """Check main health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def check_ocr_endpoint():
    """Check OCR endpoint with dummy data"""
    try:
        files = {"file": ("test.jpg", b"dummy image data", "image/jpeg")}
        response = requests.post("http://localhost:8000/ocr", files=files, timeout=30)
        
        if response.status_code == 200:
            print("✅ OCR endpoint responding")
            return True
        else:
            print(f"❌ OCR endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OCR endpoint error: {e}")
        return False

def check_translate_endpoint():
    """Check translation endpoint"""
    try:
        data = {"text": "RE ZA KU RO", "script": "LinearA"}
        response = requests.post("http://localhost:8000/translate", data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "frequency_vector" in result:
                print("✅ Translation endpoint working")
                return True
            else:
                print("❌ Translation endpoint: invalid response format")
                return False
        else:
            print(f"❌ Translation endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Translation endpoint error: {e}")
        return False

def check_narrative_endpoint():
    """Check narrative generation endpoint"""
    try:
        data = {"text": "RE ZA KU RO", "context": "ceremonial"}
        response = requests.post("http://localhost:8000/narrative", data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "narrative" in result:
                print("✅ Narrative endpoint working")
                return True
            else:
                print("❌ Narrative endpoint: invalid response format")
                return False
        else:
            print(f"❌ Narrative endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Narrative endpoint error: {e}")
        return False

def check_validate_endpoint():
    """Check validation endpoint"""
    try:
        test_frequencies = [210.42, 126.22, 157.79, 99.41]
        response = requests.post("http://localhost:8000/validate", 
                               json=test_frequencies, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "mean_frequency" in result:
                print("✅ Validation endpoint working")
                return True
            else:
                print("❌ Validation endpoint: invalid response format")
                return False
        else:
            print(f"❌ Validation endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Validation endpoint error: {e}")
        return False

def main():
    """Run comprehensive health check"""
    print("🏥 Ancient Script Universal Translator - Health Check")
    print("=" * 55)
    
    print("⏳ Waiting for server to start...")
    for i in range(30):
        try:
            requests.get("http://localhost:8000/health", timeout=2)
            break
        except:
            time.sleep(1)
    else:
        print("❌ Server not responding after 30 seconds")
        sys.exit(1)
    
    checks = [
        check_health_endpoint,
        check_ocr_endpoint,
        check_translate_endpoint,
        check_narrative_endpoint,
        check_validate_endpoint
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        time.sleep(1)  # Brief pause between checks
    
    print("\n" + "=" * 55)
    print(f"📊 Health Check Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All systems operational!")
        print("🏺 Ancient Script Universal Translator is ready!")
        sys.exit(0)
    else:
        print("⚠️ Some systems are not working properly")
        sys.exit(1)

if __name__ == "__main__":
    main()
