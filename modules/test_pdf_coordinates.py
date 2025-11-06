from simplebook_pdf_tools import extract_coordinates_from_pdf

data = extract_coordinates_from_pdf("/Users/christhomas/PycharmProjectsSimpleBook_Parser/statements/statements_ucbi_july_2024.pdf")

for item in data[:10]:
    print(item)