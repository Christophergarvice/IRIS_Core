import re

print("--- DEPOSITS (Sample Run) ---")

# Simulated snippet of text like what your UCBI statement might look like
sample_text = """
--- DEPOSITS ---
07/05 MOBILE DEPOSIT                    22,550.00
07/05 CHECK DEPOSIT                       57.20
07/08 CASH DEPOSIT                     24,350.00
07/08 TRANSFER FROM SAVINGS             8,550.00
--- OTHER CREDITS ---
"""

total = 0.0
matches = []

# Process each line
for line in sample_text.splitlines():
    match = re.search(r"(\d{2}/\d{2}).*?(\$?\d{1,3}(?:,\d{3})*\.\d{2})", line)
    if match:
        date, amount_str = match.groups()
        amount = float(amount_str.replace("$", "").replace(",", ""))

        # Flag large deposits but still include them
        if amount > 10000:
            print(f"[REVIEW] {date}: ${amount:,.2f} flagged as large deposit.")

        matches.append((date, amount))
        total += amount

# Output all deposits
for date, amount in matches:
    print(f"{date}: ${amount:,.2f}")

print(f"\nTOTAL Deposits: ${total:,.2f}")