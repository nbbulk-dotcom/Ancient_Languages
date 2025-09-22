import imagehash
from PIL import Image
import os
from .logger import log_event

def compute_phash(path):
    try:
        im = Image.open(path)
        h = imagehash.phash(im)
        return str(h)
    except Exception as e:
        log_event(f"Phash error for {path}: {e}", level="ERROR")
        return None

def deduplicate_by_key(records, key):
    seen = set()
    out = []
    for r in records:
        k = r.get(key)
        if k and k not in seen:
            seen.add(k)
            out.append(r)
    return out

def deduplicate_images(image_dir):
    hashes = {}
    duplicates = []
    for fname in os.listdir(image_dir):
        path = os.path.join(image_dir, fname)
        if not os.path.isfile(path):
            continue
        ph = compute_phash(path)
        if not ph:
            continue
        if ph in hashes:
            duplicates.append((path, hashes[ph]))
        else:
            hashes[ph] = path
    return duplicates

def compute_image_hash(image_path):
    return compute_phash(image_path)

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
