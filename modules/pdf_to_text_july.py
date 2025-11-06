import pdfplumber

input_pdf = "statements/jul24.pdf"
output_txt = "statements/statements_ucbi_july_2024_normalized.txt"

with pdfplumber.open(input_pdf) as pdf:
    all_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

with open(output_txt, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"[DONE] Saved normalized text to: {output_txt}")
