from PIL import Image
import pytesseract

image_path = r"C:\Users\tiwar\Downloads\ews.jpg"

try:
    text = pytesseract.image_to_string(Image.open(image_path))
    print("Extracted text:\n", text)
except Exception as e:
    print("Error:", e)
