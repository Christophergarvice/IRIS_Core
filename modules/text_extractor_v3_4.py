"""
text_extractor_v3_4.py
Two-pass extractor for UCBI normalized text.
First pass detects clean section ranges.
Second pass extracts transactions within each section.
"""

import re
from pathlib import Path
from cleaner import clean_text_block
from csv_loader import read_ucbi_csv
from validator import compare_totals, compare_counts, print_summary


def extract_transactions_v3_4(text):
    clean_text = clean_text_block(text)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    transactions = []

    # --- Regex patterns ---
    amount_pattern = re.compile(r"(?<!\S)\d{1,3}(?:,\d{3})*\.\d{2}(?!\S)")
    date_pattern = re.compile(r"\b\d{2}/\d{2}\b")
    header_pattern = re.compile(
        r"(-{2,}\s*(DEPOSITS?|OTHER\s+CREDITS?|CHECKS?|OTHER\s+DEBITS?)\s*-{2,})"
        r"|(^\s*\d+\s+(DEPOSITS?|CREDITS?|DEBITS?)\b)"
        r"|(\bDEPOSIT\s+TICKET\b)"
        r"|(\bOTHER\s+CREDITS?\b)"
        r"|(\bOTHER\s+DEBITS?\b)"
        r"|(\bCHECKS?\b)"
        r"|(\bDEPOSITS?\b)",
        re.I
    )

    # --- Pass 1: find section boundaries ---
    sections = []
    for i, line in enumerate(lines):
        match = header_pattern.search(line)
        if match:
            raw = match.group(0).upper()
            if "DEPOSIT" in raw and "OTHER" not in raw:
                section = "Deposits"
            elif "OTHER" in raw and "CREDIT" in raw:
                section = "Other Credits"
            elif "CHECK" in raw:
                section = "Checks"
            elif "DEBIT" in raw:
                section = "Other Debits"
            else:
                section = "Unknown"
            sections.append((section, i))
            print(f"[PASS1] Header {section} found at line {i}")
    sections.append(("END", len(lines)))

    # --- Pass 2: extract inside section boundaries ---
    for idx in range(len(sections) - 1):
        section_name, start_line = sections[idx]
        end_line = sections[idx + 1][1]
        if section_name == "END":
            continue

        for i in range(start_line, end_line):
            line = lines[i]

            # Skip noise
            if re.search(r"(TOTAL|SUMMARY|BALANCE|PAGE|FEE|MINIMUM|AVERAGE|INTEREST)", line, re.I):
                continue
            if re.search(r"DEPOSIT\s+TICKET|INDICATES A GAP IN CHECK", line, re.I):
                continue
            if line.count(".") > 4:
                continue

            # Find amounts
            amounts = amount_pattern.findall(line)
            if len(amounts) != 1:
                continue
            try:
                amount = float(amounts[0].replace(",", ""))
            except ValueError:
                continue
            if amount < 5:
                continue

            # Look for date ±5 lines
            date_match = date_pattern.search(line)
            if not date_match:
                for j in range(max(start_line, i - 5), min(end_line, i + 6)):
                    if j != i:
                        m = date_pattern.search(lines[j])
                        if m:
                            date_match = m
                            break
                if not date_match:
                    print(f"[WARN] No date found near line {i}: {line}")

            date = date_match.group() if date_match else "Unknown"
            desc = line[:line.find(amounts[0])].strip()
            transactions.append({
                "date": date,
                "description": desc,
                "amount": amount,
                "section": section_name
            })

    print(f"[DEBUG] v3_4 Extracted {len(transactions)} transactions across sections.")
    return transactions


# --- Run directly for testing ---
if __name__ == "__main__":
    txt_path = Path("statements/statements_ucbi_july_2024_normalized.txt")
    csv_path = Path("statements/AccountHistory.csv")

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_v3_4(text)
    print(f"[EXTRACTOR v3_4] Found {len(pdf_transactions)} transactions.")
    print("First few:", pdf_transactions[:10])

    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    print("[DONE] text_extractor_v3_4 finished.")