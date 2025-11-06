import os, sys
print("\n[DEBUG] CWD:", os.getcwd())
print("[DEBUG] sys.path has project?", any("SimpleBook_Parser" in p for p in sys.path))
print("[DEBUG] modules exists?", os.path.isdir(os.path.join(os.getcwd(), "modules")))
print("[DEBUG] statements exists?", os.path.isdir(os.path.join(os.getcwd(), "statements")))
print("[DEBUG] PDF exists?", os.path.exists(os.path.join(os.getcwd(), "statements", "ucbi_august_2024.pdf")))
from modules.pdf_loader import extract_text_from_pdf_auto
from modules.utils import letter_value_sum

# Path to your PDF statement
pdf_path = "statements/ucbi_august_2024.pdf"

# Extract text and note which method worked
full_text, method = extract_text_from_pdf_auto(pdf_path)

print(f"\n[INFO] Extraction method used: {method}")
print(f"\n--- First 500 characters of extracted text ---\n")
print(full_text[:500])  # preview

# Test the letter value helper
print("\nSample letter sum test:", letter_value_sum("ABC"))
from modules.pdf_loader import extract_text_from_pdf_auto
from modules.utils import letter_value_sum

# Path to your test PDF
pdf_path = "statements/ucbi_august_2024.pdf"

# Extract text and record which method worked
full_text, method = extract_text_from_pdf_auto(pdf_path)

print(f"\n[INFO] Extraction method used: {method}")
print(f"\n--- First 500 characters of extracted text ---\n")
print(full_text[:500])  # preview

# Example: use letter_value_sum on a sample string
print("\nSample letter sum test:", letter_value_sum("ABC"))
from modules.cleaner import clean_text_block
print("\n[INFO] Cleaned sample text:\n", clean_text_block(full_text[:500]))
from modules.csv_loader import read_ucbi_csv

from modules.normalizer import normalize_passes

normalized_text = normalize_passes(full_text)
print("\n[INFO] Normalized text sample:\n", normalized_text[:500])
# --- Debug: save full normalized text for pattern study ---
with open("normalized_debug.txt", "w", encoding="utf-8") as f:
    f.write(normalized_text)
print("[DEBUG] Saved normalized text to normalized_debug.txt")
csv_path = "statements/AccountHistory.csv"
rows = read_ucbi_csv(csv_path)
print(f"[CSV LOADER] Loaded {len(rows)} transactions.")
print("First few:", rows[:5])
from modules.extractor import extract_transactions_from_text

# --- Extract from PDF text ---
pdf_transactions = extract_transactions_from_text(normalized_text)
print(f"[EXTRACTOR] Found {len(pdf_transactions)} transactions in PDF.")
print("First few:", pdf_transactions[:5])

# --- Compare to CSV totals ---
from modules.validator import compare_totals, compare_counts, print_summary
from modules.csv_loader import read_ucbi_csv

csv_path = "statements/AccountHistory.csv"
csv_rows = read_ucbi_csv(csv_path)
loose_amounts = extract_amounts_loose(text)
print(f"[DEBUG] Found {len(loose_amounts)} total amounts (loose scan).")
print("First few amounts:", loose_amounts[:20])
match, pdf_total, csv_total, diff = compare_totals(pdf_transactions, csv_rows)
pdf_count, csv_count = compare_counts(pdf_transactions, csv_rows)
print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count)