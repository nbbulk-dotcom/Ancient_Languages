from datetime import datetime

def parse_sigla_api(signs):
    parsed = []
    for sign in signs:
        glyph = {
            "sign_id": sign.get("id", "").upper(),
            "sign_name": sign.get("name", ""),
            "unicode_value": sign.get("unicode", None),
            "character_image": None,
            "frequency_count": sign.get("frequency", 0),
            "contexts": sign.get("contexts", []),
            "variants": sign.get("variants", []),
            "transliteration": sign.get("transliteration", ""),
            "classification": sign.get("classification", ""),
            "image_url": sign.get("image_url", None),
            "sources": [{
                "source_name": "SigLA", 
                "url": "https://sigla.phis.me/api/signs", 
                "fetched_at": datetime.utcnow().isoformat()
            }]
        }
        parsed.append(glyph)
    return parsed

def parse_gorila_pdf(pdf_text):
    parsed = []
    lines = pdf_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) >= 2:
                glyph = {
                    "sign_id": parts[0].upper(),
                    "sign_name": parts[1] if len(parts) > 1 else "",
                    "unicode_value": None,
                    "character_image": None,
                    "frequency_count": int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0,
                    "contexts": [],
                    "variants": [],
                    "transliteration": parts[3] if len(parts) > 3 else "",
                    "classification": "GORILA",
                    "sources": [{
                        "source_name": "GORILA", 
                        "url": "GORILA Transcriptions PDF", 
                        "fetched_at": datetime.utcnow().isoformat()
                    }]
                }
                parsed.append(glyph)
    
    return parsed
