import fitz  # PyMuPDF

# Replace with your actual PDF file path
pdf_path = r"C:\Users\tiwar\Downloads\AgroGuard_AI_Synopsis MAIN.pdf"

doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text[:500])  # print first 500 characters of each page
