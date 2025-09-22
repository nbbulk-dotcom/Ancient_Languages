import json
import csv
import os
from .logger import log_event

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    log_event(f"Saved JSON -> {path}")

def save_csv(list_of_dicts, path, fieldnames=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not list_of_dicts:
        with open(path, "w") as f:
            f.write("")
        log_event(f"Saved empty CSV -> {path}")
        return
    if fieldnames is None:
        keys = set()
        for d in list_of_dicts:
            keys.update(d.keys())
        fieldnames = sorted(keys)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in list_of_dicts:
            writer.writerow({k: (row.get(k) if row.get(k) is not None else "") for k in fieldnames})
    log_event(f"Saved CSV -> {path}")

def save_image_bytes(b, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b)
    log_event(f"Saved image -> {path}")

def save_image(image_bytes, path):
    save_image_bytes(image_bytes, path)
