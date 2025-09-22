import json, os, subprocess, time, hashlib

def git_commit_sha():
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"]).decode().strip()
    except Exception:
        return None

def make_provenance(inputs:list, note:str=None):
    obj = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "commit_sha": git_commit_sha(),
        "inputs": inputs,
        "note": note,
    }
    obj["manifest_hash"] = hashlib.sha1(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    return obj
