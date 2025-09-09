# main.py
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from extract import extract_text
from summarize import summarize_text
from collections import Counter
import re
def extract_keywords(text, top_n=10):
    # Split words, ignore common stopwords
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set([
        "the","and","is","in","to","of","a","for","with","on",
        "as","by","an","from","that","this","are","be","it","its"
    ])
    words = [w for w in words if w not in stopwords]
    most_common = Counter(words).most_common(top_n)
    return [word for word, _ in most_common]



load_dotenv()

app = FastAPI(title="Document Summarizer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.staticfiles import StaticFiles
import os

# Serve the frontend static files (index.html etc.)
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
async def home():
    return {"message": "Welcome to the Document Summarizer API. Go to /docs to upload a file."}

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    summary_length: str = Form("medium")  # user can choose short/medium/long
):
    try:
        # Save uploaded file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Extract text (PDF/image)
        text = extract_text(file_path)

        # Step 2: Summarize
        summary = summarize_text(text, length=summary_length)

        # ✅ Step 3: Extract keywords from summary
        keywords = extract_keywords(summary, top_n=15)

        # Clean up uploaded file
        os.remove(file_path)

        # Step 4: Return everything
        return {
            "filename": file.filename,
            "extracted_text": text[:1000],  # preview first 1000 chars
            "summary": summary,
            "keywords": keywords
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
