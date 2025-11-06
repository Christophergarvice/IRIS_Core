"""
extractor.py
Extracts transactions from UCBI PDF text.
Detects 'Deposits', 'Other Credits', 'Checks', and 'Other Debits' sections,
then pulls Date, Description, and Amount.
"""

import re
from modules.cleaner import clean_text_block

# --- Core extractor ---
def extract_transactions_from_text(text):
    """
    Parse the cleaned PDF text into structured transactions.
    Returns list of dicts: {date, description, amount, section}
    """
    clean_text = clean_text_block(text)

    # Normalize dashes and headers
    clean_text = re.sub(r"—+", "-", clean_text)
    clean_text = re.sub(r"\s+-\s+", "-", clean_text)

    # Find sections like --- DEPOSITS --- or --- OTHER DEBITS ---
    sections = re.split(r"-{2,}\s*([A-Z ]{5,})\s*-{2,}", clean_text)
    transactions = []
    current_section = None

    for part in sections:
        part = part.strip()
        if not part:
            continue
        if part.isupper() and len(part) < 40:
            current_section = part.title().strip()
            continue

        # Extract rows with date + amount pattern
        lines = [l.strip() for l in part.split("\n") if l.strip()]
        for line in lines:
            match = re.search(r"(\d{2}/\d{2})[^\d]*(\d{1,3}(?:,\d{3})*\.\d{2})", line)
            if match:
                date = match.group(1)
                amount_str = match.group(2).replace(",", "")
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue
                # Use everything before the amount as description
                desc = line[: match.start(2)].strip()
                transactions.append(
                    {
                        "date": date,
                        "description": desc,
                        "amount": amount,
                        "section": current_section or "Unknown",
                    }
                )

    return transactions


# --- Quick test when run standalone ---
if __name__ == "__main__":
    import pdfplumber
    from pathlib import Path


def extract_transactions_from_text(text):
    clean_text = clean_text_block(text)

    # Split sections like --- DEPOSITS --- or --- OTHER DEBITS ---
    sections = re.split(r"-{2,}\s*([A-Z ]{5,})\s*-{2,}", clean_text)
    transactions = []
    current_section = None

    for part in sections:
        part = part.strip()
        if not part:
            continue
        if part.isupper() and len(part) < 40:
            current_section = part.title().strip()
            continue

        # Skip headers like "CHECK # DATE AMOUNT"
        if "CHECK #" in part or "DATE" in part and "AMOUNT" in part:
            continue

        # More flexible pattern for date + amount
        pattern = re.compile(
            r"(\d{2}[\-/]\d{2})[^\d]{0,40}?(\d{1,3}(?:,\d{3})*\.\d{2})",
            re.MULTILINE
        )

        for m in pattern.finditer(part):
            date = m.group(1)
            amount = float(m.group(2).replace(",", ""))
            start = max(0, m.start() - 30)
            desc = part[start:m.start()].strip()
            transactions.append({
                "date": date,
                "description": desc,
                "amount": amount,
                "section": current_section or "Unknown"
            })

    print(f"[DEBUG] Found {len(transactions)} potential matches in extractor.")
    return transactions