import requests
import time
from urllib.parse import urlparse
import yaml
from pathlib import Path
from .logger import log_event

_config = {}
_try_load = True
RATE_LIMITS = {}

def load_config(path="config.yaml"):
    global _config, RATE_LIMITS, _try_load
    if not _try_load:
        return
    _try_load = False
    p = Path(path)
    if p.exists():
        with p.open("r", encoding="utf-8") as f:
            _config = yaml.safe_load(f)
            RATE_LIMITS.update(_config.get("rate_limits", {}))

def get_rate_limit_for_host(host):
    load_config()
    return RATE_LIMITS.get(host, RATE_LIMITS.get("default", 1.0))

def safe_get(url, headers=None, params=None, timeout=30, allow_retry=True):
    host = urlparse(url).netloc
    delay = get_rate_limit_for_host(host)
    time.sleep(delay)
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        log_event(f"HTTP GET failed: {url} - {e}", level="ERROR")
        if allow_retry:
            time.sleep(2)
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=timeout)
                resp.raise_for_status()
                return resp
            except Exception as e2:
                log_event(f"Retry failed: {url} - {e2}", level="ERROR")
                raise
        raise

def get_rate_limit(host):
    return get_rate_limit_for_host(host)

def set_rate_limits(limits):
    global RATE_LIMITS
    RATE_LIMITS.update(limits)

def rate_limited_get(url, headers=None):
    return safe_get(url, headers=headers)
