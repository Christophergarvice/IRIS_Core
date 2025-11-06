"""
cleaner.py
Removes OCR/PDF noise and standardizes extracted text.
Also supports optional numeric signature mapping for pattern analysis.
"""

import re
import string

def clean_text_block(text: str) -> str:
    """
    Remove junk symbols, normalize spacing, and trim lines.
    """
    # Remove non-printable characters
    text = ''.join(c for c in text if c in string.printable)

    # Replace common OCR mistakes (customize as needed)
    replacements = {
        '£': 'E',
        '4nRCE': 'MERCE',
        'DQmmmOa': 'ACCOUNT',
        'ObInII,e,fJ': '',
        'COba': 'COMMERCE',
        'uDBI': 'UCBI',
        'udbi': 'UCBI',
        'DOCUWNTS': 'DOCUMENTS',
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Remove stray punctuation clusters like '==', '::', '--'
    text = re.sub(r'[-=:_]{2,}', ' ', text)

    # Normalize spaces and line breaks
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()


def numeric_signature(text: str) -> list[int]:
    """
    Return a list of numeric codes representing the text's characters.
    Useful for comparing damaged OCR lines.
    """
    return [ord(c) for c in text if c.isalnum()]


def compare_signatures(a: list[int], b: list[int], tolerance: int = 10) -> bool:
    """
    Compare two numeric signatures to see if they represent similar text.
    Returns True if their total value difference is within 'tolerance'.
    """
    return abs(sum(a) - sum(b)) <= tolerance


# Simple test when run directly
if __name__ == "__main__":
    sample = "COba4nRCE GA 30529"
    print("[RAW]  ", sample)
    print("[CLEAN]", clean_text_block(sample))
    print("[SIGNATURE]", numeric_signature(sample))

