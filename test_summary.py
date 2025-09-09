from extract import extract_text
from summarize import summarize_text

# Test with a sample document (PDF or Image)
file_path = r"C:\Users\tiwar\Downloads\resume (5).pdf"  # <-- replace with your own test file

# Step 1: Extract text
text = extract_text(file_path)
print("\n✅ Extracted Text (first 300 chars):\n", text[:300], "...")

# Step 2: Summarize text
summary = summarize_text(text)
print("\n📌 Summary:\n", summary)
