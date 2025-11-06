import csv
from datetime import datetime

def _parse_amount(value):
    if not value:
        return 0.0
    v = value.replace(",", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0

def read_ucbi_csv(path):
    """Reads UCBI CSV with columns: Account Number, Post Date, Check, Description, Debit, Credit, Status, Balance, Classification"""
    records = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            debit = _parse_amount(row.get("Debit"))
            credit = _parse_amount(row.get("Credit"))
            amount = credit - debit
            record = {
                "date": datetime.strptime(row["Post Date"], "%m/%d/%Y").strftime("%Y-%m-%d"),
                "description": row.get("Description", "").strip(),
                "amount": round(amount, 2),
                "balance": _parse_amount(row.get("Balance")),
                "classification": row.get("Classification", "").strip(),
            }
            records.append(record)
    return records