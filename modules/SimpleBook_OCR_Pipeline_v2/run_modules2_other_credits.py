import sys
import re

file_path = sys.argv[1] if len(sys.argv) > 1 else "../../statements/statements_ucbi_july_2024_normalized.txt"

print("\n--- OTHER CREDITS ---")


with open(file_path, "r") as f:
    lines = f.readlines()

pattern = re.compile(r"^\s*(\d{2}/\d{2}).*?(\$[\d,]+\.\d{2})")
matches = []

for line in lines:
    m = pattern.search(line)
    if m:
        matches.append(m.groups())

total = 0.0
for date, amount in matches:
    print(f"{date}: {amount}")
    total += float(amount.replace("$", "").replace(",", ""))

print(f"\nTOTAL Other Credits: ${total:,.2f}")
# --- Locate Other Credits Section ---
start = end = None
for i, line in enumerate(lines):
    if "OTHERCREDITS" in line.upper() or "OTHER CREDITS" in line.upper():
        start = i + 1
    elif start is not None and (
        "CHECKS" in line.upper() or
        "OTHER DEBITS" in line.upper() or
        "DEPOSITS" in line.upper()
    ):
        end = i
        break

if start is None or end is None:
    print("[ERROR] Other Credits section not found.")
    exit()

credit_lines = lines[start:end]

# --- Parse Amounts and Dates ---
date_pattern = re.compile(r"\b(\d{2}/\d{2})\b")
credits = []


for line in credit_lines:
    clean_line = re.sub(r"\s+", " ", line)
    date_match = date_pattern.search(clean_line)
    if date_match:
        last_date = date_match.group(1)

    amounts = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", clean_line)
    if not amounts:
        continue

    for amt_str in set(amounts):
        amount = float(amt_str.replace(",", ""))
        if last_date:
            credits.append((last_date, amount))

# --- Output ---
print("\n--- OTHER CREDITS ---")
for date, amount in credits:
    print(f"{date}: ${amount:,.2f}")

print(f"\nTOTAL Other Credits: ${sum(a for _, a in credits):,.2f}")