import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.pdf_parser import extract_text_from_pdf

def parse_harappa_archive(url):
    parsed = []
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        script_elements = soup.find_all(['div', 'span', 'p'], class_=re.compile(r'.*script.*|.*glyph.*|.*sign.*', re.I))
        
        for element in script_elements:
            text = element.get_text(strip=True)
            if text and len(text) < 50:
                glyph = {
                    "sign_id": f"H-{len(parsed)+1:03d}",
                    "sign_name": f"Indus Valley Sign {len(parsed)+1}",
                    "unicode_value": None,
                    "character_image": None,
                    "frequency_count": 1,
                    "contexts": [url],
                    "variants": [],
                    "transliteration": text,
                    "classification": "Harappa Archive",
                    "sources": [{
                        "source_name": "Harappa Archive", 
                        "url": url, 
                        "fetched_at": datetime.utcnow().isoformat()
                    }]
                }
                parsed.append(glyph)
                
                if len(parsed) >= 100:
                    break
                    
    except Exception as e:
        print(f"Harappa Archive parsing error: {e}")
    
    return parsed

def parse_mahadevan_concordance(pdf_path):
    parsed = []
    try:
        text = extract_text_from_pdf(pdf_path)
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and re.match(r'^[0-9]+', line):
                parts = line.split()
                if len(parts) >= 2:
                    glyph = {
                        "sign_id": f"M-{parts[0]}",
                        "sign_name": f"Mahadevan Sign {parts[0]}",
                        "unicode_value": None,
                        "character_image": None,
                        "frequency_count": int(parts[1]) if parts[1].isdigit() else 1,
                        "contexts": [],
                        "variants": [],
                        "transliteration": parts[2] if len(parts) > 2 else "",
                        "classification": "Mahadevan Concordance",
                        "sources": [{
                            "source_name": "Mahadevan Concordance", 
                            "url": pdf_path, 
                            "fetched_at": datetime.utcnow().isoformat()
                        }]
                    }
                    parsed.append(glyph)
                    
    except Exception as e:
        print(f"Mahadevan Concordance parsing error: {e}")
    
    return parsed
