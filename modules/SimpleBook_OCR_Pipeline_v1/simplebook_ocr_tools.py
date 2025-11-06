import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
from PIL import Image
import pdf2image
import os

def extract_text_from_scanned_pdf(path):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return []

    print(f"[INFO] Running OCR on: {path}")

    # Tell pdf2image exactly where Poppler is
    poppler_path = "/opt/homebrew/bin"

    pages = pdf2image.convert_from_path(path, poppler_path=poppler_path)
    results = []

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, config="--psm 6")
        results.append(text)
        print(f"[PAGE {i+1}] {len(text)} characters recognized")

    print(f"[INFO] OCR complete – {len(results)} pages processed.")
    return results