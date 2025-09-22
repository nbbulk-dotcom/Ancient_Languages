import os
import requests

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return dest_path
