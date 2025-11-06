"""
text_extractor.py
Reads the normalized text file instead of the raw PDF and extracts transactions.
"""

import re
from pathlib import Path
from modules.cleaner import clean_text_block
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary

def extract_transactions_from_normalized_text(text):
    clean_text = clean_text_block(text)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    transactions = []
    pattern = re.compile(r"(\d{2}/\d{2})[^\d\n]{0,25}?(\d{1,3}(?:,\d{3})*\.\d{2})")

    section = None
    for line in lines:
        if "---" in line and any(x in line.upper() for x in ["DEPOSIT", "CREDIT", "CHECK", "DEBIT"]):
            section = line.strip("- ").title()
            continue

        match = pattern.search(line)
        if match:
            date = match.group(1)
            amount = float(match.group(2).replace(",", ""))
            desc = line[:match.start(2)].strip()
            transactions.append({
                "date": date,
                "description": desc,
                "amount": amount,
                "section": section or "Unknown"
            })

    print(f"[DEBUG] Extracted {len(transactions)} transactions from normalized text.")
    return transactions


if __name__ == "__main__":
    txt_path = Path("statements/statements_ucbi_august_2024_normalized.txt")
    csv_path = Path("statements/AccountHistory.csv")

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_from_normalized_text(text)
    print(f"[EXTRACTOR] Found {len(pdf_transactions)} transactions in normalized text.")
    print("First few:", pdf_transactions[:5])

    # --- Loose amount scan ---
    def extract_amounts_loose(text):
        """Find all standalone amounts in the text, even if dates are missing."""
        pattern = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")
        return [float(a.replace(",", "")) for a in pattern.findall(text)]

    loose_amounts = extract_amounts_loose(text)
    print(f"[DEBUG] Found {len(loose_amounts)} total amounts (loose scan).")
    print("First few amounts:", loose_amounts[:20])

    # --- Validate totals ---
    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)