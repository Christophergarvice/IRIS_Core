import sys
import os
import re

# -----------------------------------------------------------
# Module 4 - OTHER DEBITS
# Parses the expenses section from UCBI bank statements
# -----------------------------------------------------------

DEFAULT_FILE = "/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/ocr_july_cleaned_v2.txt"

file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

if not os.path.exists(file_path):
    print(f"[ERROR] Input file not found: {file_path}")
    sys.exit(1)

print(f"[INFO] Using input file: {file_path}")

with open(file_path, "r") as f:
    lines = f.readlines()

# -----------------------------------------------------------
# Locate OTHER DEBITS section
# -----------------------------------------------------------
# -----------------------------------------------------------
# Locate ALL OTHER DEBITS sections (multi-page)
# -----------------------------------------------------------

section_starts = []
section_ends = []

for i, line in enumerate(lines):
    if "OTHER DEBITS" in line.upper():
        section_starts.append(i + 1)

# If no sections found:
if not section_starts:
    print("[ERROR] OTHER DEBITS section not found.")
    sys.exit(1)

# Find the next major header *after* each start
for start in section_starts:
    for j in range(start, len(lines)):
        if (
            "DAILY BALANCE" in lines[j].upper()
            or "CHECKS" in lines[j].upper()
            or "DEPOSITS" in lines[j].upper()
            or "OTHER CREDITS" in lines[j].upper()
        ):
            section_ends.append(j)
            break

# Pair starts and ends
combined_lines = []
for start, end in zip(section_starts, section_ends):
    combined_lines.extend(lines[start:end])

debit_lines = combined_lines
# -----------------------------------------------------------
# Clean continuation markers
# -----------------------------------------------------------

cleaned_lines = []
for line in debit_lines:
    if "*** CONTINUED" in line.upper():
        continue
    cleaned_lines.append(line.rstrip())
debit_lines = cleaned_lines

# -----------------------------------------------------------
# Parse each line
# Format pattern:
#   DESCRIPTION TEXT...   07/10   109.74
# -----------------------------------------------------------

amount_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*\.\d{2})")
date_pattern = re.compile(r"\b(\d{2}/\d{2})\b")

parsed = []

for raw in debit_lines:
    line = " ".join(raw.split())  # normalize spaces

    # Amount must be present to count this line
    amt_match = amount_pattern.search(line)
    if not amt_match:
        continue

    amount = float(amt_match.group(1).replace(",", ""))

    # Try to find the date
    date_match = date_pattern.search(line)
    date = date_match.group(1) if date_match else "UNKNOWN"

    # Description = everything before the amount
    desc = line[:amt_match.start()].strip()

    parsed.append((date, amount, desc))

# -----------------------------------------------------------
# OUTPUT
# -----------------------------------------------------------

print("\n--- OTHER DEBITS ---")

total = 0.0

for date, amount, desc in parsed:
    print(f"{date} | ${amount:,.2f} | {desc}")
    total += amount

print(f"\nTOTAL Other Debits: ${total:,.2f}")