"""
pdf_loader.py
Handles automatic PDF text extraction.
Tries PDFMiner first, then falls back to OCR if text layer is missing.
"""

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract

def ocr_extract(pdf_path):
    """Extract text from a scanned PDF using OCR."""
    images = convert_from_path(pdf_path)
    text_blocks = [pytesseract.image_to_string(img) for img in images]
    return "\n".join(text_blocks)

def extract_text_from_pdf_auto(pdf_path, min_text_chars=500):
    """
    Try PDFMiner first; if no usable text found, switch to OCR.
    Returns extracted text and which method was used.
    """
    try:
        text = extract_text(pdf_path)
        if len(text.strip()) < min_text_chars:
            print(f"[INFO] Low text length ({len(text.strip())}) — switching to OCR.")
            text = ocr_extract(pdf_path)
            method = "OCR"
        else:
            print("[INFO] Used PDFMiner successfully.")
            method = "PDFMiner"
    except Exception as e:
        print(f"[WARN] PDFMiner failed ({e}) — using OCR.")
        text = ocr_extract(pdf_path)
        method = "OCR"

    return text, method