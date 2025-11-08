# validate_ocr_pipeline.py
import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

PDF_PATH = "/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_july_2024.pdf"
POPLER_BIN = "/opt/homebrew/bin"  # where poppler binaries are installed

def validate():
    if not os.path.exists(PDF_PATH):
        print(f"[ERROR] PDF not found: {PDF_PATH}")
        return

    print(f"[INFO] Converting PDF to images: {PDF_PATH}")
    try:
        pages = convert_from_path(PDF_PATH,
                                  dpi=200,
                                  poppler_path=POPLER_BIN,
                                  fmt="ppm",
                                  single_file=False)
    except Exception as e:
        print(f"[ERROR] PDF conversion failed: {e}")
        return

    print(f"[INFO] {len(pages)} page(s) converted to images")

    # Run OCR on first page only for test
    page0 = pages[0]
    text = pytesseract.image_to_string(page0, config="--psm 6")
    print(f"[INFO] OCR text sample (first 300 chars):\n{text[:300]!r}")

    print("[INFO] Validation complete")

if __name__ == "__main__":
    validate()