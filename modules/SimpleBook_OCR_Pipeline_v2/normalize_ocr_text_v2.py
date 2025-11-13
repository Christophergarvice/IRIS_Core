import re
import os

STATEMENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "statements")

RAW_FILES = {
    "july": os.path.join(STATEMENTS_DIR, "ocr_july_raw.txt"),
    "august": os.path.join(STATEMENTS_DIR, "ocr_august_raw.txt"),
}

OUTPUT_FILES = {
    "july": os.path.join(STATEMENTS_DIR, "ocr_july_cleaned_v2.txt"),
    "august": os.path.join(STATEMENTS_DIR, "ocr_august_cleaned_v2.txt"),
}

# Garbage patterns to remove from OCR
GARBAGE_REGEX = r"[=<>~“”‘’—–]|shee|eS|eK|eo|s\+"

SECTION_HEADERS = {
    "DEPOSITS": "--- DEPOSITS ---",
    "OTHER CREDITS": "--- OTHER CREDITS ---",
    "OTHER DEBITS": "--- OTHER DEBITS ---",
    "CHECKS": "--- CHECKS ---",
}

def clean_line(line: str) -> str:
    # Remove OCR garbage
    line = re.sub(GARBAGE_REGEX, "", line)

    # Normalize spacing
    line = re.sub(r"\s{2,}", " ", line.strip())

    # Drop tiny garbage lines with no numbers
    if len(line) < 4 and not any(c.isdigit() for c in line):
        return ""

    # Fix section headers by keyword detection
    upper_line = line.upper()
    for key, replacement in SECTION_HEADERS.items():
        if key in upper_line:
            return replacement

    return line


def clean_file(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"[ERROR] Missing file: {input_path}")
        return

    print(f"[INFO] Cleaning {input_path}")

    cleaned_lines = []
    with open(input_path, "r") as f:
        for raw_line in f:
            cleaned = clean_line(raw_line)
            if cleaned.strip():
                cleaned_lines.append(cleaned)

    with open(output_path, "w") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[DONE] Wrote cleaned file to {output_path}\n")


def main():
    for month in RAW_FILES:
        clean_file(RAW_FILES[month], OUTPUT_FILES[month])


if __name__ == "__main__":
    main()