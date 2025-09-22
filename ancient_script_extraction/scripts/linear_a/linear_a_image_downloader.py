import requests

def download_linear_a_images(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content
