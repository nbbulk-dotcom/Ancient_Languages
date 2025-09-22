import requests, time, logging
from typing import Optional

log = logging.getLogger("robust_get")
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

def robust_get(url: str, headers: Optional[dict]=None, timeout: int=20,
               retries: int=5, backoff: float=2.0, allow_empty: bool=False):
    for attempt in range(1, retries+1):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            status = r.status_code
            if 200 <= status < 300:
                if (not allow_empty) and (r.text.strip() == "" or r.text.strip() == "[]"):
                    log.warning("Empty response body from %s (attempt %s)", url, attempt)
                    raise RuntimeError("Empty response")
                return r
            else:
                log.warning("HTTP %s from %s (attempt %s)", status, url, attempt)
        except Exception as e:
            log.warning("Attempt %s failed for %s: %s", attempt, url, str(e))
        time.sleep(backoff * (2 ** (attempt-1)))
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts")
