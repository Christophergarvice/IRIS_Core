"""
text_extractor_v3.py
Structured extractor for normalized UCBI text.
Identifies Deposits, Other Credits, Checks, and Other Debits.
Pairs dates and amounts within each section.
"""

import re
from pathlib import Path
from modules.cleaner import clean_text_block
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary


def split_into_sections(text):
    """Divide the normalized text into sections based on headers."""
    sections = {
        "Deposits": "",
        "Other Credits": "",
        "Checks": "",
        "Other Debits": "",
    }

    current = None
    for line in text.splitlines():
        line_upper = line.upper()
        if "DEPOSITS" in line_upper:
            current = "Deposits"
        elif "OTHER CREDITS" in line_upper:
            current = "Other Credits"
        elif "CHECKS" in line_upper:
            current = "Checks"
        elif "OTHER DEBITS" in line_upper:
            current = "Other Debits"
        elif current:
            sections[current] += line + "\n"

    return sections


def extract_transactions_from_section(section_name, text):
    """Extract date and amount pairs from a given text section."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    transactions = []
    amount_pattern = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")
    date_pattern = re.compile(r"\d{2}/\d{2}")

    for i, line in enumerate(lines):
        if re.search(r"balance|continued|page|total|summary|statement", line, re.I):
            continue

        amount_match = amount_pattern.search(line)
        if not amount_match:
            continue

        amount = float(amount_match.group().replace(",", ""))
        date_match = date_pattern.search(line)
        if not date_match:
            # look ±2 lines for a nearby date
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j == i:
                    continue
                m = date_pattern.search(lines[j])
                if m:
                    date_match = m
                    break

        date = date_match.group() if date_match else "Unknown"
        desc = line[:amount_match.start()].strip()

        transactions.append({
            "date": date,
            "description": desc,
            "amount": amount,
            "section": section_name
        })

    return transactions


def extract_transactions_v3(text):
    """Full structured extractor."""
    clean = clean_text_block(text)
    sections = split_into_sections(clean)
    all_tx = []

    for name, content in sections.items():
        if content.strip():
            txs = extract_transactions_from_section(name, content)
            all_tx.extend(txs)

    print(f"[DEBUG] v3 Extracted {len(all_tx)} total transactions across {len(sections)} sections.")
    return all_tx


if __name__ == "__main__":
    txt_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_august_2024_normalized.txt")
    csv_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/AccountHistory.csv")

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_v3(text)
    print(f"[EXTRACTOR v3] Found {len(pdf_transactions)} transactions.")
    print("First few:", pdf_transactions[:10])

    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    print("[DONE] text_extractor_v3 finished.")