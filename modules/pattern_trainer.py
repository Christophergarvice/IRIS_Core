"""
text_extractor.py
Reads and extracts transactions from a normalized .txt version of a UCBI statement.
Used for debugging OCR or PDFMiner output when the raw PDF is hard to parse.
"""

from modules.extractor import extract_transactions_from_text
from modules.cleaner import clean_text_block
from modules.validator import compare_totals, compare_counts, print_summary
from modules.csv_loader import read_ucbi_csv
from pathlib import Path

def run_text_extractor():
    # Path to your normalized text file
    text_path = Path("statements/Normalized text.txt")
    if not text_path.exists():
        print("[ERROR] Normalized text file not found:", text_path)
        return

    # Read text file
    with open(text_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Clean and extract transactions
    print("[INFO] Cleaning text and extracting transactions...")
    cleaned = clean_text_block(text)
    transactions = extract_transactions_from_text(cleaned)
    print(f"[INFO] Found {len(transactions)} transactions in normalized text.")
    print("First few:", transactions[:5])

    # Compare against CSV data
    csv_path = Path("statements/AccountHistory.csv")
    if csv_path.exists():
        csv_rows = read_ucbi_csv(csv_path)
        match, pdf_total, csv_total, diff = compare_totals(transactions, csv_rows)
        pdf_count, csv_count = compare_counts(transactions, csv_rows)
        print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)
    else:
        print("[WARN] No CSV file found for comparison.")

# Run if called directly
if __name__ == "__main__":
    run_text_extractor()