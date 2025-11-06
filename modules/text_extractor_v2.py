"""
text_extractor_v2.py
Smarter extractor for normalized UCBI text.
Finds amounts and nearby dates within ±2 lines.
"""

import re
from pathlib import Path
from modules.cleaner import clean_text_block
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary


def extract_transactions_v2(text):
    clean_text = clean_text_block(text)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    transactions = []

    amount_pattern = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")
    date_pattern = re.compile(r"\d{2}/\d{2}")
    for i, line in enumerate(lines):
        # Skip obvious non-transaction lines
        if re.search(
                r"balance|average|minimum|days|period|total|page|credits|debits|summary|statement|service|fee|interest",
                line, re.I):
            continue

        amount_match = amount_pattern.search(line)
        if not amount_match:
            continue

        # Ignore tiny or isolated numbers (like 1.00 or 4.96 on headers)
        amount = float(amount_match.group().replace(",", ""))
        if amount < 5:  # skip small fragments
            continue

        date_match = date_pattern.search(line)
        if not date_match:
            # look ±2 lines for nearby date
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j == i:
                    continue
                m = date_pattern.search(lines[j])
                if m:
                    date_match = m
                    break

        # Only count if a valid date is found nearby
        if not date_match:
            continue

        date = date_match.group()
        desc = line[: amount_match.start()].strip()
        transactions.append({
            "date": date,
            "description": desc,
            "amount": amount,
            "section": "v2-Extracted"
        })

    print(f"[DEBUG] v2 Extracted {len(transactions)} transactions.")
    return transactions


# --- run directly ---
if __name__ == "__main__":
    txt_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_august_2024_normalized.txt")
    csv_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/AccountHistory.csv")

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_v2(text)
    print(f"[EXTRACTOR v2] Found {len(pdf_transactions)} transactions.")
    print("First few:", pdf_transactions[:10])

    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    print("[DONE] text_extractor_v2 finished.")