import json
from datetime import datetime
import threading

_lock = threading.Lock()

def log_event(message, path="extraction_log.txt", level="INFO", extra=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "message": message
    }
    if extra:
        entry["extra"] = extra
    line = json.dumps(entry, ensure_ascii=False)
    with _lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
