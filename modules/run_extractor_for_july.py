# run_extractor_for_july.py
from pathlib import Path
from text_extractor_v3_4 import extract_transactions_v3_4
from csv_loader import read_ucbi_csv
from validator import compare_totals, compare_counts, print_summary

# --- File paths ---
txt_path = Path("statements/statements_ucbi_july_2024_normalized.txt")
csv_path = Path("statements/AccountHistory.csv")  # optional if you have one for July

# --- Check text file exists ---
if not txt_path.exists():
    print(f"[ERROR] Text file not found: {txt_path}")
    exit()

# --- Run Extractor ---
text = txt_path.read_text(errors="ignore")
pdf_transactions = extract_transactions_v3_4(text)
print(f"[EXTRACTOR v3_4] Found {len(pdf_transactions)} transactions.")
print("First few:", pdf_transactions[:10])

# --- Optional comparison to CSV ---
if csv_path.exists():
    csv_rows = read_ucbi_csv(csv_path)
    match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
    pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
    print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)

print("[DONE] run_extractor_for_july.py finished.")