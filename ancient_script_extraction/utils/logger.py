import json
import os
from datetime import datetime

def log_event(message, path="extraction_log.txt"):
    timestamp = datetime.utcnow().isoformat()
    entry = {"timestamp": timestamp, "message": message}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + "\n")
