#!/usr/bin/env python3
"""
Final deployment test for Ancient Script Universal Translator
Tests the complete system with the provided image attachment
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

def test_with_provided_image():
    """Test OCR with the provided image.png attachment"""
    print("🖼️ Testing with provided image attachment...")
    
    attachment_path = None
    possible_paths = [
        "/home/ubuntu/attachments/384a24d3-96f9-476c-af2f-1168151017f0/image.png",
        "~/attachments/384a24d3-96f9-476c-af2f-1168151017f0/image.png",
        "../attachments/384a24d3-96f9-476c-af2f-1168151017f0/image.png"
    ]
    
    for path in possible_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            attachment_path = expanded_path
            break
    
    if not attachment_path:
        print("⚠️ Image attachment not found, creating test image...")
        import cv2
        import numpy as np
        
        img = np.ones((300, 600, 3), dtype=np.uint8) * 255
        cv2.putText(img, 'RE ZA KU RO', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        cv2.putText(img, 'Linear A Test', (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
        
        attachment_path = '/tmp/test_ancient_script.png'
        cv2.imwrite(attachment_path, img)
        print(f"   Created test image: {attachment_path}")
    else:
        print(f"   Found image attachment: {attachment_path}")
    
    try:
        with open(attachment_path, 'rb') as f:
            files = {"file": ("ancient_script.png", f, "image/png")}
            
            print("   Testing OCR endpoint...")
            response = requests.post("http://localhost:8000/ocr", files=files, timeout=30)
            
            if response.status_code == 200:
                ocr_data = response.json()
                extracted_text = ocr_data.get('extracted_text', '')
                print(f"   ✅ OCR successful: {extracted_text}")
                
                print("   Testing translation endpoint...")
                trans_data = {"text": extracted_text, "script": "linear_a"}
                trans_response = requests.post("http://localhost:8000/translate", data=trans_data, timeout=15)
                
                if trans_response.status_code == 200:
                    trans_result = trans_response.json()
                    print(f"   ✅ Translation successful: {len(trans_result.get('frequency_vector', []))} glyphs analyzed")
                    
                    print("   Testing narrative endpoint...")
                    narr_data = {"text": extracted_text, "context": "ceremonial"}
                    narr_response = requests.post("http://localhost:8000/narrative", data=narr_data, timeout=15)
                    
                    if narr_response.status_code == 200:
                        narr_result = narr_response.json()
                        print(f"   ✅ Narrative successful: {len(narr_result.get('narrative', ''))} characters")
                        return True
                    else:
                        print(f"   ❌ Narrative failed: {narr_response.status_code}")
                else:
                    print(f"   ❌ Translation failed: {trans_response.status_code}")
            else:
                print(f"   ❌ OCR failed: {response.status_code}")
                print(f"   Response: {response.text}")
        
        return False
        
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False
    finally:
        if attachment_path == '/tmp/test_ancient_script.png' and os.path.exists(attachment_path):
            os.remove(attachment_path)

def test_academic_downloads():
    """Test academic PDF downloads"""
    print("📚 Testing academic downloads...")
    
    try:
        response = requests.get("http://localhost:8000/downloads/Brett_Methodology.pdf", timeout=10)
        if response.status_code == 200:
            print("   ✅ Brett_Methodology.pdf accessible")
        else:
            print(f"   ❌ Brett_Methodology.pdf failed: {response.status_code}")
            return False
        
        response = requests.get("http://localhost:8000/downloads/Brett_License.pdf", timeout=10)
        if response.status_code == 200:
            print("   ✅ Brett_License.pdf accessible")
            return True
        else:
            print(f"   ❌ Brett_License.pdf failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Download test error: {e}")
        return False

def test_frontend_access():
    """Test frontend accessibility"""
    print("🌐 Testing frontend access...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Frontend accessible")
            return True
        else:
            print(f"   ❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend test error: {e}")
        return False

def main():
    """Run final deployment test"""
    print("🏺 Ancient Script Universal Translator - Final Deployment Test")
    print("=" * 70)
    
    print("⏳ Waiting for server to start...")
    for i in range(30):
        try:
            requests.get("http://localhost:8000/health", timeout=2)
            print("✅ Server is ready")
            break
        except:
            time.sleep(1)
    else:
        print("❌ Server not responding after 30 seconds")
        return False
    
    tests = [
        ("Frontend Access", test_frontend_access),
        ("Academic Downloads", test_academic_downloads),
        ("Complete Pipeline with Image", test_with_provided_image),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🧪 Running {name}...")
        if test_func():
            passed += 1
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print(f"📊 Final Deployment Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for public deployment!")
        print("\n🚀 Deployment URLs:")
        print("   • Local: http://localhost:8000")
        print("   • Academic Downloads: http://localhost:8000/downloads/")
        print("   • API Documentation: http://localhost:8000/docs")
        return True
    else:
        print("⚠️ Some tests failed. Please review before public deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
