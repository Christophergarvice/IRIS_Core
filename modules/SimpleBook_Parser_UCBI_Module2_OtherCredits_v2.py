import sys
import os
import re

# Default to July cleaned v2 file if no argument is provided
DEFAULT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "statements", "ocr_july_cleaned_v2.txt")
)

def load_lines(path: str):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)
    with open(path, "r") as f:
        return f.readlines()

def find_other_credits_section(lines):
    start = end = None

    for i, line in enumerate(lines):
        u = line.upper()

        # Start at OTHER CREDITS header
        if "OTHER CREDITS" in u and start is None:
            start = i + 1
            continue

        # Stop when we hit the next section header
        if start is not None and (
            "CHECKS" in u
            or "OTHER DEBITS" in u
            or "DEPOSITS" in u
        ):
            end = i
            break

    if start is None or end is None:
        print("[ERROR] Other Credits section not found.")
        sys.exit(1)

    return lines[start:end]

def parse_other_credits(lines):
    """
    Parse OTHER CREDITS section from cleaned v2 text.
    - Dates look like: 07/03
    - Amounts look like: 650.00 or 1,500.00
    - Continuation lines may not have date or amount.
    """
    date_pattern = re.compile(r"\b(\d{2}/\d{2})\b")
    amount_pattern = re.compile(r"\d{1,3}(?:,\d{3})*\.\d{2}")

    credits = []
    last_date = None

    for raw in lines:
        line = " ".join(raw.split()).strip()
        if not line:
            continue

        # If line contains a date, update last_date
        m_date = date_pattern.search(line)
        if m_date:
            last_date = m_date.group(1)

        # Extract monetary amounts
        amounts = amount_pattern.findall(line)
        if not amounts:
            continue

        # Attach each amount to the most recent date
        for amt_str in amounts:
            amount = float(amt_str.replace(",", ""))
            if last_date is None:
                continue
            credits.append((last_date, amount, line))

    return credits

def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    print(f"[INFO] Using input file: {file_path}")

    lines = load_lines(file_path)
    section_lines = find_other_credits_section(lines)
    credits = parse_other_credits(section_lines)

    if not credits:
        print("[WARN] No OTHER CREDITS found in section.")
        return

    print("\n--- OTHER CREDITS (parsed) ---")
    for date, amount, line in credits:
        print(f"{date}: ${amount:,.2f}  |  {line}")

    total = sum(a for _, a, _ in credits)
    print(f"\nTOTAL Other Credits: ${total:,.2f}")

if __name__ == "__main__":
    main()