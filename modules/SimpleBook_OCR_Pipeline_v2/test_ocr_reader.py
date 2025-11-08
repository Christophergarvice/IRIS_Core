import os
from simplebook_ocr_tools import extract_text_from_scanned_pdf

def main():
    path = "/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_july_2024.pdf"
    abs_path = os.path.abspath(path)
    out_dir = os.path.dirname(os.path.abspath("../statements/"))
    out_path = os.path.join(out_dir, "ocr_output_raw.txt")

    # Create the statements folder if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    print(f"[INFO] Running OCR on: {abs_path}")

    pages = extract_text_from_scanned_pdf(path)

    # Combine all pages
    full_text = "\n\n".join(pages)

    # Save raw OCR text
    with open(out_path, "w") as f:
        f.write(full_text)
    print(f"[INFO] Saved raw OCR text to {out_path}")

    print("\n--- OCR PREVIEW ---\n")
    print(full_text[:500])

    print(f"\n[INFO] Total pages: {len(pages)}")

if __name__ == "__main__":
    main()
