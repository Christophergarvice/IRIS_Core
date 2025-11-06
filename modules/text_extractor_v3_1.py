"""
text_extractor_v3_1.py
Enhanced version of v3.
Improves header detection, date recovery, and classification for broken UCBI normalized statements.
"""

import re
from pathlib import Path
from modules.cleaner import clean_text_block
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary


def extract_transactions_v3_1(text):
    clean_text = clean_text_block(text)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    transactions = []

    # --- patterns ---
    amount_pattern = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")
    date_pattern = re.compile(r"\d{2}/\d{2}")

    # handle noisy headers like ---DEPOSITS--- or - - OTHER DEBITS - -
    header_pattern = re.compile(
        r"-+\s*(DEPOSITS?|OTHER\s+CREDITS?|CHECKS?|OTHER\s+DEBITS?)\s*-+", re.I
    )

    section = "Unknown"
    last_date = None

    for i, line in enumerate(lines):
        # detect header section
        hmatch = header_pattern.search(line)
        if hmatch:
            section = hmatch.group(1).strip().title()
            continue

        # skip obvious non-transaction text
        if re.search(
            r"(balance|average|minimum|days|period|page|total|summary|service|interest|account|telephone)",
            line,
            re.I,
        ):
            continue

        # find all amounts on line
        amatch = amount_pattern.search(line)
        if not amatch:
            continue

        amount = float(amatch.group().replace(",", ""))
        if amount < 1:
            continue

        # locate date on same or nearby line
        dmatch = date_pattern.search(line)
        if not dmatch:
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j == i:
                    continue
                m = date_pattern.search(lines[j])
                if m:
                    dmatch = m
                    break

        date = dmatch.group() if dmatch else (last_date or "Unknown")
        last_date = date if date != "Unknown" else last_date

        desc = line[: amatch.start()].strip()
        transactions.append(
            {
                "date": date,
                "description": desc,
                "amount": amount,
                "section": section,
            }
        )

    print(f"[DEBUG] v3_1 Extracted {len(transactions)} transactions across sections.")
    return transactions


if __name__ == "__main__":
    txt_path = Path(
        "/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_august_2024_normalized.txt"
    )
    csv_path = Path(
        "/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/AccountHistory.csv"
    )

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_v3_1(text)
    print(f"[EXTRACTOR v3_1] Found {len(pdf_transactions)} transactions.")
    print("First few:", pdf_transactions[:10])

    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    print("[DONE] text_extractor_v3_1 finished.")