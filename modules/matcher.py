# matcher.py
# Compares normalized text transactions to CSV transactions

from pathlib import Path
from modules.text_extractor import extract_transactions_from_normalized_text
from modules.csv_loader import read_ucbi_csv
from modules.validator import compare_totals, compare_counts, print_summary

txt_path = Path("../statements/statements_ucbi_august_2024_normalized.txt")
csv_path = Path("../statements/AccountHistory.csv")

if not txt_path.exists():
    print("[ERROR] Normalized text file not found:", txt_path)
    exit()

text = txt_path.read_text(errors="ignore")
pdf_transactions = extract_transactions_from_normalized_text(text)
print(f"[MATCHER] Found {len(pdf_transactions)} transactions in normalized text.")
print("First few:", pdf_transactions[:5])

csv_rows = read_ucbi_csv(csv_path)
print(f"[MATCHER] Found {len(csv_rows)} transactions in CSV.")

match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)