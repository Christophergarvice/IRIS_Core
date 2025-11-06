"""
validator.py
Compares parsed PDF data to digital CSV ground truth.
Checks totals, transaction counts, and can later verify categories.
"""

def sum_amounts(rows):
    """Sum the 'amount' field safely."""
    return round(sum(r.get("amount", 0.0) for r in rows), 2)

def compare_totals(pdf_rows, csv_rows, tolerance=0.01):
    """
    Compare the overall totals between PDF and CSV.
    Returns tuple (match: bool, pdf_total, csv_total, difference).
    """
    pdf_total = sum_amounts(pdf_rows)
    csv_total = sum_amounts(csv_rows)
    diff = round(csv_total - pdf_total, 2)
    match = abs(diff) <= tolerance
    return match, pdf_total, csv_total, diff

def compare_counts(pdf_rows, csv_rows):
    """Compare how many transactions each source detected."""
    return len(pdf_rows), len(csv_rows)

def print_summary(match, pdf_total, csv_total, diff, pdf_count, csv_count):
    print("\n--- VALIDATOR SUMMARY ---")
    print(f"PDF transactions: {pdf_count}")
    print(f"CSV transactions: {csv_count}")
    print(f"PDF total: ${pdf_total:,.2f}")
    print(f"CSV total: ${csv_total:,.2f}")
    print(f"Difference: ${diff:,.2f}")
    print(f"Match within tolerance? {'✅ YES' if match else '❌ NO'}")