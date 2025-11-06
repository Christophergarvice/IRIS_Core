"""
text_extractor_v3_2.py
Improved section-aware extractor for UCBI normalized text.
Detects Deposits, Other Credits, Checks, and Other Debits with tighter amount validation.
"""

import re
from pathlib import Path
from modules.cleaner import clean_text_block
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary


def extract_transactions_v3_2(text):
    clean_text = clean_text_block(text)
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    transactions = []

    amount_pattern = re.compile(r"\b\d{1,3}(?:,\d{3})*\.\d{2}\b")
    date_pattern = re.compile(r"\b\d{2}/\d{2}\b")
    # Patterns
    amount_pattern = re.compile(r"\b\d{1,3}(?:,\d{3})*\.\d{2}\b")
    date_pattern = re.compile(r"\b\d{2}/\d{2}\b")
    header_pattern = re.compile(
        r"(-{1,}\s*(DEPOSITS?|OTHER\s+CREDITS?|CHECKS?|OTHER\s+DEBITS?)\s*-{1,}|"
        r"\b\d+\s+(DEPOSITS?|CREDITS?|DEBITS?)\b|"
        r"\bDEPOSIT\s+TICKET\b)",
        re.I
    )

    current_section = None

    for i, line in enumerate(lines):
        # Debug header detection
        if re.search(r"DEPOSIT|CREDIT|CHECK|DEBIT", line, re.I):
            print(f"[DEBUG HEADER TEST] Line {i}: {line}")

        header_match = header_pattern.search(line)
        if header_match:
            raw_header = header_match.group(0).upper()
            if "DEPOSIT" in raw_header and "OTHER" not in raw_header:
                current_section = "Deposits"
            elif "OTHER" in raw_header and "CREDIT" in raw_header:
                current_section = "Other Credits"
            elif "CHECK" in raw_header:
                current_section = "Checks"
            elif "DEBIT" in raw_header:
                current_section = "Other Debits"
            else:
                current_section = "Unknown"
            print(f"[DEBUG] Switched section → {current_section}  (line {i})")
            continue  # Skip to next line after section switch

        if not current_section:
            continue

        # Skip headers, summaries, and bank noise lines
        if re.search(r"\b\d+\s+(DEBITS?|CREDITS?)\b", line, re.I):
            continue
        if re.search(r"\b(TOTAL|SUMMARY|BALANCE|PAGE)\b", line, re.I):
            continue
        if re.search(r"\b\d{1,3}(?:,\d{3})*\.\d{2}\s+\d{1,3}(?:,\d{3})*\.\d{2}\b", line):
            continue
        if re.search(r"^\d+\s+(CREDIT|DEBIT|DEPOSITS?)\b", line, re.I):
            continue
        if re.search(r"DEPOSIT\s+TICKET", line, re.I):
            continue
        if re.search(r"INDICATES A GAP IN CHECK", line, re.I):
            continue
        if re.search(r"balance|page|summary|minimum|average|interest|service|fee", line, re.I):
            continue

        # Handle multiple amounts on the same line (side-by-side entries)
        amounts = amount_pattern.findall(line)
        if len(amounts) > 1:
            for amt in amounts:
                transactions.append({
                    "date": "Unknown",
                    "description": line[: line.find(amt)].strip(),
                    "amount": float(amt.replace(",", "")),
                    "section": current_section
                })
            continue  # move to next line after processing multi-amounts
        if not amount_match:
            continue
        amount = float(amount_match.group().replace(",", ""))
        if amount < 5:
            continue

        # Find date (same or nearby line)
        date_match = date_pattern.search(line)
        if not date_match:
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
            "section": current_section
        })

    print(f"[DEBUG] v3_2 Extracted {len(transactions)} transactions across sections.")
    return transactions

# --- Run directly ---
if __name__ == "__main__":
    txt_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_august_2024_normalized.txt")
    csv_path = Path("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/AccountHistory.csv")

    if not txt_path.exists():
        print("[ERROR] Normalized text file not found.")
        exit()

    text = txt_path.read_text(errors="ignore")
    pdf_transactions = extract_transactions_v3_2(text)
    print(f"[EXTRACTOR v3_2] Found {len(pdf_transactions)} transactions.")
    print("First few:", pdf_transactions[:10])

    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    print("[DONE] text_extractor_v3_2 finished.")