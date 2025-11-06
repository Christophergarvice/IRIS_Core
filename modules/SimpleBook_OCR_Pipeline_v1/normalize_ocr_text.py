import re

def normalize_ocr_text(raw_text: str) -> str:
    # Merge accidental spaces within numbers like "5 , 620 . 00"
    text = re.sub(r"(\d)\s*,\s*(\d{3})\s*\.\s*(\d{2})", r"\1,\2.\3", raw_text)
    text = re.sub(r"(\d)\s*\.\s*(\d{2})", r"\1.\2", text)

    # Collapse double spaces and line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n", text)

    # Join words broken by OCR artifacts (like COMMU NITY → COMMUNITY)
    text = re.sub(r"([A-Z])\s+([A-Z])", r"\1\2", text)

    # Remove page headers like "BUSINESS FREEDOM ACCOUNT XXXXXXXXXXX4609"
    text = re.sub(r"BUSINESS\s+FREEDOM\s+ACCOUNT.*", "", text, flags=re.I)

    return text.strip()


if __name__ == "__main__":
    with open("../../statements/ocr_output_raw.txt", "r") as f:
        raw = f.read()
    cleaned = normalize_ocr_text(raw)
    with open("../../statements/ocr_output_cleaned.txt", "w") as f:
        f.write(cleaned)
    print("[INFO] Cleaned text saved to ocr_output_cleaned.txt")