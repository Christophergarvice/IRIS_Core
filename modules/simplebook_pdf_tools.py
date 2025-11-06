# simplebook_pdf_tools.py
# SimpleBook Library v1 – Core PDF Extraction and Normalization Tools

import pypdfium2 as pdfium
import os

def extract_coordinates_from_pdf(path):
    """
    Extract text and coordinates (x, y) from each page of a PDF.
    Uses pypdfium2 for precise position data.
    Returns a list of dicts: [{page, x, y, text}, ...]
    """

    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return []

    results = []
    try:
        pdf = pdfium.PdfDocument(path)
        page_count = len(pdf)
        print(f"[INFO] Reading {page_count} pages from {path}")

        for page_index in range(page_count):
            page = pdf[page_index]
            textpage = page.get_textpage()

            for n in range(textpage.count_rects()):
                rect = textpage.get_rect(n)

                # Handle nested tuple forms ((left, top, right, bottom),)
                if isinstance(rect[0], (tuple, list)):
                    rect = rect[0]

                try:
                    left, top, right, bottom = map(float, rect)
                except Exception:
                    continue

                try:
                    text = textpage.get_text_bounded((left, top, right, bottom))
                except Exception:
                    continue

                if text and text.strip():
                    results.append({
                        "page": page_index + 1,
                        "x": left,
                        "y": bottom,
                        "text": text.strip()
                    })

            textpage.close()

        pdf.close()
        print(f"[INFO] Extracted {len(results)} text elements total.")
        return results

    except Exception as e:
        print(f"[ERROR] Failed to extract coordinates: {e}")
        return []