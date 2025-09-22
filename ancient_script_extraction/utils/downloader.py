import os
from .logger import log_event
import requests

def download_binary(url, dest_path, timeout=30):
    try:
        r = requests.get(url, stream=True, timeout=timeout)
        r.raise_for_status()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        log_event(f"Downloaded {url} -> {dest_path}")
        return dest_path
    except Exception as e:
        log_event(f"Download failed {url}: {e}", level="ERROR")
        raise

def download_file(url, dest_path, timeout=30):
    return download_binary(url, dest_path, timeout)
