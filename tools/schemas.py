from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Provenance(BaseModel):
    timestamp: str
    commit_sha: str
    inputs: List[Dict[str, Any]]
    note: str
    method: str

class TranslateResult(BaseModel):
    extracted_text: str
    glyphs: List[Dict[str, Any]]
    frequency_vector: List[float]
    narrative: str
    confidence_score: float
    provenance: Provenance
