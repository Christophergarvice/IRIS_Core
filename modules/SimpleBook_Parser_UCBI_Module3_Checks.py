import sys
import re
import os

# -----------------------------------------------------------
# Module 3 - CHECKS
# Parses the 3-column check table from UCBI bank statements
# -----------------------------------------------------------

DEFAULT_FILE = "../statements/ocr_july_cleaned_v2.txt"

file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

if not os.path.exists(file_path):
    print(f"[ERROR] Input file not found: {file_path}")
    sys.exit(1)

print(f"[INFO] Using input file: {file_path}")

with open(file_path, "r") as f:
    lines = f.readlines()

# -----------------------------------------------------------
# Locate CHECKS section
# -----------------------------------------------------------
start = end = None

for i, line in enumerate(lines):
    if "CHECKS" in line.upper():
        start = i + 1
        continue

    if start is not None and (
            "OTHER DEBITS" in line.upper() or
            "DEPOSITS" in line.upper() or
            "OTHER CREDITS" in line.upper()
    ):
        end = i
        break

if start is None or end is None:
    print("[ERROR] CHECKS section not found.")
    sys.exit(1)

check_lines = lines[start:end]

# -----------------------------------------------------------
# Parse check entries (3-column table)
# Example:
# 873*07/02 942.67   892 07/05 60.13   896*07/23 300.00
# -----------------------------------------------------------

check_pattern = re.compile(
    r"(?P<num>\d{1,5}\*?)\s*(?P<date>\d{2}/\d{2})\s+(?P<amount>\d{1,3}(?:,\d{3})*\.\d{2})"
)

checks = []

for line in check_lines:
    for match in check_pattern.finditer(line):
        num = match.group("num")
        date = match.group("date")
        amt_str = match.group("amount")
        amount = float(amt_str.replace(",", ""))

        checks.append((num, date, amount))

# -----------------------------------------------------------
# Detect check number sequence gaps
# -----------------------------------------------------------

cleaned_nums = [int(c[0].replace("*", "")) for c in checks]
cleaned_nums_sorted = sorted(cleaned_nums)

missing_numbers = []
for i in range(len(cleaned_nums_sorted) - 1):
    curr = cleaned_nums_sorted[i]
    nxt = cleaned_nums_sorted[i + 1]

    if nxt - curr > 1:
        for gap in range(curr + 1, nxt):
            missing_numbers.append(gap)

# -----------------------------------------------------------
# Output
# -----------------------------------------------------------

print("\n--- CHECKS ---")

for num, date, amount in checks:
    print(f"Check #{num} | {date} | ${amount:,.2f}")

total_amount = sum(a for _, _, a in checks)
print(f"\nTOTAL Checks: ${total_amount:,.2f}")

if missing_numbers:
    print("\nMissing check numbers:")
    print(", ".join(str(n) for n in missing_numbers))
else:
    print("\nNo check number gaps detected.")