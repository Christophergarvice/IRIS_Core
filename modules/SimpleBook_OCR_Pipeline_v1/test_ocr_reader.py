from simplebook_ocr_tools import extract_text_from_scanned_pdf
import os

def main():
    path = "../../statements/statements_ucbi_july_2024.pdf"
    abs_path = os.path.abspath(path)
    print(f"[INFO] Running OCR on: {abs_path}")

    pages = extract_text_from_scanned_pdf(path)

    # Combine all pages
    full_text = "\n\n".join(pages)

    # Save raw OCR text
    out_path = os.path.join("../../statements", "ocr_output_raw.txt")
    with open(out_path, "w") as f:
        f.write(full_text)
    print(f"[INFO] Saved raw OCR text to {out_path}")

    # Preview first 500 characters
    print("\n--- OCR PREVIEW ---\n")
    print(full_text[:500])

    print(f"\n[INFO] Total pages: {len(pages)}")

if __name__ == "__main__":
    main()