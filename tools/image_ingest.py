import os, json, cv2, hashlib
from pathlib import Path

def ensure_dir(p): Path(p).mkdir(parents=True, exist_ok=True)

def preprocess_image(in_path, out_path, dpi_scale=2):
    img = cv2.imread(in_path, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"Failed to open {in_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    h, w = clean.shape
    clean_resized = cv2.resize(clean, (w*dpi_scale, h*dpi_scale), interpolation=cv2.INTER_CUBIC)
    ensure_dir(os.path.dirname(out_path))
    cv2.imwrite(out_path, clean_resized)
    return out_path

def ingest_folder(src_folder, dst_folder, manifest_path):
    ensure_dir(dst_folder)
    manifest = []
    for fn in sorted(os.listdir(src_folder)):
        if not fn.lower().endswith((".png",".jpg",".jpeg","tif","tiff")):
            continue
        src = os.path.join(src_folder, fn)
        dst = os.path.join(dst_folder, fn)
        preprocess_image(src, dst)
        sha = hashlib.sha1(open(dst,"rb").read()).hexdigest()
        manifest.append({"file": dst, "sha1": sha, "source": src})
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    p.add_argument("--dst", required=True)
    p.add_argument("--manifest", required=True)
    args = p.parse_args()
    ingest_folder(args.src, args.dst, args.manifest)
