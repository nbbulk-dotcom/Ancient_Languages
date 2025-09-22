from datetime import datetime
import re

def parse_cdli_api(tablets):
    parsed = []
    glyph_set = set()
    
    for tablet in tablets:
        if 'transliteration' in tablet:
            transliteration = tablet['transliteration']
            glyphs = extract_proto_elamite_glyphs(transliteration)
            
            for glyph_id in glyphs:
                if glyph_id not in glyph_set:
                    glyph_set.add(glyph_id)
                    glyph = {
                        "sign_id": glyph_id,
                        "sign_name": f"Proto-Elamite Sign {glyph_id}",
                        "unicode_value": None,
                        "character_image": None,
                        "frequency_count": 1,
                        "contexts": [tablet.get('id', '')],
                        "variants": [],
                        "transliteration": glyph_id,
                        "classification": "CDLI",
                        "tablet_id": tablet.get('id', ''),
                        "sources": [{
                            "source_name": "CDLI", 
                            "url": "https://cdli.ucla.edu/api/", 
                            "fetched_at": datetime.utcnow().isoformat()
                        }]
                    }
                    parsed.append(glyph)
    
    return parsed

def extract_proto_elamite_glyphs(transliteration):
    glyph_pattern = r'M\d{3}[a-z]?'
    glyphs = re.findall(glyph_pattern, transliteration)
    return list(set(glyphs))
