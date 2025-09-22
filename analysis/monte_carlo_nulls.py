import json, numpy as np, random
from pathlib import Path

def load_vectors(path):
    return json.load(open(path))

def preserve_frequency_permutation(signs, base_vals):
    perm = base_vals.copy()
    random.shuffle(perm)
    return dict(zip(signs, perm))

def compute_similarity(vectors, templates, sign_to_hz):
    import numpy as np
    sims = []
    for v in vectors:
        freqs = [sign_to_hz.get(s, 0.0) for s in v.get("sign_sequence", [])]
        if not freqs:
            sims.append(0.0); continue
        base = freqs[0] if freqs[0]>0 else 1.0
        ratios = np.log(np.array(freqs)/base)
        best = 0.0
        for t in templates:
            tvec = np.log(np.array(t["normalized"]))
            if len(ratios)>=len(tvec):
                for i in range(len(ratios)-len(tvec)+1):
                    win = ratios[i:i+len(tvec)]
                    sim = float(np.dot(win,tvec)/(np.linalg.norm(win)*np.linalg.norm(tvec)+1e-12))
                    best = max(best, sim)
        sims.append(best)
    return np.mean(sims)

def run_nulls(vectors_path, templates_path, sign_inventory_path, trials=1000, out_path="null.npy"):
    vectors = load_vectors(vectors_path)
    templates = json.load(open(templates_path))
    signs = list(json.load(open(sign_inventory_path)).keys())
    base_vals = list(range(1, len(signs)+1))
    nulls = []
    for t in range(trials):
        sign_to_hz = preserve_frequency_permutation(signs, base_vals)
        score = compute_similarity(vectors, templates, sign_to_hz)
        nulls.append(score)
        if t % 100 == 0:
            print("trial",t,"score",score)
    import numpy as np
    np.save(out_path, np.array(nulls))
    return out_path
