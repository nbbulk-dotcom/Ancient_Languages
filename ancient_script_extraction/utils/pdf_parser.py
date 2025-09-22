import pdfplumber
import io
from .logger import log_event

def extract_text_from_pdf_bytes(pdf_bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
            return "\n".join(pages)
    except Exception as e:
        log_event(f"PDF parse failed: {e}", level="ERROR")
        raise

def extract_text_from_pdf_path(path):
    try:
        with pdfplumber.open(path) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
            return "\n".join(pages)
    except Exception as e:
        log_event(f"PDF parse failed: {path} - {e}", level="ERROR")
        raise

def extract_text_from_pdf(pdf_path):
    return extract_text_from_pdf_path(pdf_path)
