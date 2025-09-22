import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_unicode_block(start_code, end_code):
    start_int = int(start_code.replace("U+", ""), 16)
    end_int = int(end_code.replace("U+", ""), 16)
    
    parsed = []
    for code_point in range(start_int, end_int + 1):
        try:
            char = chr(code_point)
            glyph = {
                "sign_id": f"U+{code_point:04X}",
                "sign_name": f"Khitan Large Script Character {code_point:04X}",
                "unicode_value": f"U+{code_point:04X}",
                "character": char,
                "character_image": None,
                "frequency_count": 0,
                "contexts": [],
                "variants": [],
                "transliteration": "",
                "classification": "Unicode Block",
                "sources": [{
                    "source_name": "Unicode", 
                    "url": f"Unicode Block U+18B00–U+18CFF", 
                    "fetched_at": datetime.utcnow().isoformat()
                }]
            }
            parsed.append(glyph)
        except ValueError:
            continue
    
    return parsed

def parse_babelstone(url):
    parsed = []
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    glyph = {
                        "sign_id": cells[0].get_text(strip=True),
                        "sign_name": cells[1].get_text(strip=True),
                        "unicode_value": cells[0].get_text(strip=True) if cells[0].get_text(strip=True).startswith('U+') else None,
                        "character_image": None,
                        "frequency_count": 0,
                        "contexts": [],
                        "variants": [],
                        "transliteration": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                        "classification": "BabelStone",
                        "sources": [{
                            "source_name": "BabelStone", 
                            "url": url, 
                            "fetched_at": datetime.utcnow().isoformat()
                        }]
                    }
                    parsed.append(glyph)
    except Exception as e:
        print(f"BabelStone parsing error: {e}")
    
    return parsed
