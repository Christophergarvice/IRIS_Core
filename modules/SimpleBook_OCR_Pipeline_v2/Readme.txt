SimpleBook OCR Pipeline — Developer + Builder Reference

1. Purpose
Convert scanned bank statements into structured financial data for the SimpleBook system.
This version processes scanned PDFs using OCR (Tesseract + Poppler) and extracts clean, parse-ready text.

2. Pipeline Overview
   1. test_ocr_reader.py
      • Runs OCR on a scanned PDF.
      • Outputs ocr_output_raw.txt to /statements/.
      • Dependencies: pdf2image, pytesseract, Poppler, and Tesseract installed system-wide.
   2. normalize_ocr_text.py
      • Cleans and formats the OCR output.
      • Removes irregular spacing, fixes line breaks, and saves ocr_output_cleaned.txt.
   3. run_modules1_deposits.py
      • Reads the cleaned text and extracts deposit entries.
      • Uses regex patterns to detect dates and dollar amounts.
      • Prints each deposit and totals them.
      • Output is validated against statement totals.
   4. simplebook_ocr_tools.py
      • Holds reusable OCR functions.
      • Used by the test reader script.
      • Future versions will host text detection and section parsing tools.

Directory Structure
SimpleBook_Parser/
│
├── modules/
│   ├── test_ocr_reader.py
│   ├── normalize_ocr_text.py
│   ├── run_modules1_deposits.py
│   ├── simplebook_ocr_tools.py
│
└── statements/
    ├── statements_ucbi_july_2024.pdf
    ├── ocr_output_raw.txt
    └── ocr_output_cleaned.txt

4. Running the System
   1. Run OCR on a scanned statement:
      python modules/test_ocr_reader.py
   2. Normalize the text:
      python modules/normalize_ocr_text.py
   3. Extract deposits:
      python modules/run_modules1_deposits.py
      Example output:
      --- DEPOSITS ---
      07/05: $7,200.00
      07/08: $550.00
      ...
      TOTAL Deposits: $12,550.00

5. How to Use Each Module
Module 1 – test_ocr_reader.py
   1. Place your scanned bank-statement PDF in the statements/ folder (e.g., statements_ucbi_august_2024.pdf).
   2. Ensure dependencies are installed: pdf2image, pytesseract, Poppler, Tesseract.
   3. Run:
      python modules/test_ocr_reader.py
   4. This generates ocr_output_raw.txt in the statements/ folder.
   5. Confirm output looks reasonable (text extracted, pages captured).

Module 2 – normalize_ocr_text.py
   1. Input: statements/ocr_output_raw.txt.
   2. Run:
      python modules/normalize_ocr_text.py
   3. Output: statements/ocr_output_cleaned.txt.
   4. Verify: line breaks are resolved, spacing normalized, no obvious garbage.

Module 3 – run_modules1_deposits.py
   1. Input: statements/ocr_output_cleaned.txt.
   2. Run:
      python modules/run_modules1_deposits.py
   3. The script will parse deposit entries by date and amount using regex patterns.
   4. It will print each detected deposit and a total.
   5. Compare the printed total with the official statement’s deposit total for reconciliation.

Module 4 – simplebook_ocr_tools.py
   1. This module provides helper functions (e.g. image preprocessing, text normalization) used by the other scripts.
   2. It is not typically invoked directly by the user.
   3. If you extend the pipeline (e.g., adding checks, other credits), you will import and use functions from this file.

6. Notes
• Each module is standalone and testable.
• If OCR output is mis-aligned (characters missing, lines broken incorrectly):
    - Increase the DPI when converting PDF pages to images.
    - Use a Tesseract config with --psm 6 (or other page segmentation modes) to improve layout detection.
• If regex in run_modules1_deposits.py fails to capture some entries:
    - Inspect ocr_output_cleaned.txt to see actual formatting.
    - Adjust regex patterns to match variations (different date formats, thousands separators, parentheses for negative amounts).
• Maintain the same structure for future modules (Other Credits, Checks, Other Debits).
• Maintain versioning: update README when you add modules or change patterns.
• Keep backups of ocr_output_raw.txt before re-running normalization in case you want to compare or revert.