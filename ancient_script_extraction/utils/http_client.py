import requests
import time
from urllib.parse import urlparse

RATE_LIMITS = {}

def get_rate_limit(host):
    return RATE_LIMITS.get(host, 1)

def set_rate_limits(limits):
    global RATE_LIMITS
    RATE_LIMITS = limits

def rate_limited_get(url, headers=None):
    host = urlparse(url).netloc
    delay = get_rate_limit(host)
    time.sleep(delay)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response
