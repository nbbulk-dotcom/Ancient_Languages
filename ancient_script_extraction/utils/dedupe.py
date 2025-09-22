import hashlib
from PIL import Image
import imagehash

def compute_image_hash(image_path):
    image = Image.open(image_path)
    return str(imagehash.phash(image))

def normalize_sign_id(sign_id):
    return sign_id.strip().upper().replace(" ", "_")

def deduplicate_glyphs(glyphs):
    seen_hashes = set()
    seen_ids = set()
    unique_glyphs = []
    
    for glyph in glyphs:
        sign_id = normalize_sign_id(glyph.get('sign_id', ''))
        
        if sign_id in seen_ids:
            continue
            
        if glyph.get('character_image'):
            try:
                img_hash = compute_image_hash(glyph['character_image'])
                if img_hash in seen_hashes:
                    continue
                seen_hashes.add(img_hash)
            except Exception:
                pass
                
        seen_ids.add(sign_id)
        unique_glyphs.append(glyph)
    
    return unique_glyphs
