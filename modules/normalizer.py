import re
from string import ascii_uppercase

# Map A–Z → 1–26
LETTER_TO_NUM = {ch: i for i, ch in enumerate(ascii_uppercase, 1)}

def text_to_number_pattern(text: str) -> list[int]:
    """Convert letters to numbers and preserve digits."""
    result = []
    for ch in text.upper():
        if ch.isalpha():
            result.append(LETTER_TO_NUM[ch])
        elif ch.isdigit():
            result.append(int(ch))
    return result

def normalize_text_pass(text: str) -> str:
    """Replace OCR letter noise and common UCBI artifacts with clean equivalents."""
    substitutions = {
        "COba": "Com",
        "COMMERCEMERCE": "COMMERCE",
        "CObnCUNITY": "COMMUNITY",
        "DOCUWNTS": "DOCUMENTS",
        "nB": "NB",
        "nQmOCQQQQ{": "4609",  # account ending normalization
        "UDBI": "UCBI"
    }
    for bad, good in substitutions.items():
        text = text.replace(bad, good)
    text = re.sub(r"[^A-Z0-9/\.\,\-\s]", "", text.upper())  # clean symbols
    return text

def normalize_passes(text: str, passes: int = 2) -> str:
    """Run multiple normalization passes."""
    for _ in range(passes):
        text = normalize_text_pass(text)
    return text