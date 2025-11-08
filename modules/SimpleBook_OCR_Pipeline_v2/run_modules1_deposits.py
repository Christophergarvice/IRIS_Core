# SimpleBook_Parser_UCBI_Module1 - Enhanced Lookahead Deposit Parser
import re

# --- Load Normalized OCR Text ---
with open("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/ocr_output_cleaned.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

# --- Locate Deposits Section ---
start = end = None
for i, line in enumerate(lines):
    if start is None and "DEPOSITS" in line.upper():
        start = i + 1
    elif start is not None and (
        "OTHER CREDITS" in line.upper()
        or "CHECKS" in line.upper()
        or "OTHER DEBITS" in line.upper()
    ):
        end = i
        break

if start is None or end is None:
    print("[ERROR] Deposits section not found.")
    exit()

# isolate only deposit section
deposit_lines = lines[start:end]

# --- Regex Pattern ---
date_pattern = re.compile(r"\b(\d{2}/\d{2})\b")
deposits = []
last_date = None

# --- Parse Deposits ---
for line in deposit_lines:
    # Fix UCBI-style number format like '7 .200 . 00' -> '7,200.00'
    clean_line = re.sub(r"(\d)\s*\.\s*(\d{3})\s*\.\s*(\d{2})", r"\1,\2.\3", line)
    clean_line = re.sub(r"\s+", " ", clean_line)  # normalize spaces

    # Capture date
    date_match = date_pattern.search(clean_line)
    if date_match:
        last_date = date_match.group(1)

    # Capture single amount per occurrence
    amount_matches = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", clean_line)
    if not amount_matches:
        continue

    # Take only unique values per line
    for amt_str in set(amount_matches):
        amount = float(amt_str.replace(",", ""))
        if amount > 10000:
            print(f"[REVIEW] {last_date or 'Unknown'}: ${amount:,.2f} flagged as large deposit.")
        if last_date:
            deposits.append((last_date, amount))

# --- Print Results ---
print("\n--- DEPOSITS ---")
for date, amount in deposits:
    print(f"{date}: ${amount:,.2f}")

print(f"\nTOTAL Deposits: ${sum(a for _, a in deposits):,.2f}")