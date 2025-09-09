# extract.py
import os
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import io

# Path to Tesseract (only needed for OCR fallback)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file_path):
    """
    Extract text from a PDF or image.
    Uses PyMuPDF for text-based PDFs, and Tesseract OCR for scanned PDFs/images.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            # 1. Try normal text extraction
            page_text = page.get_text("text")
            if page_text.strip():
                text += page_text + " "
            else:
                # 2. Fallback: OCR for scanned page
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text += pytesseract.image_to_string(img) + " "
        doc.close()

    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

    else:
        raise ValueError("Unsupported file format. Use PDF or image.")

    return text.replace("\n", " ").strip()
