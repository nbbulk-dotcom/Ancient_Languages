import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
from robust_get import robust_get

def download_linear_a_images(url):
    response = robust_get(url, timeout=30, retries=3, allow_empty=False)
    return response.content
