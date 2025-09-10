# main.py
import uvicorn
import os
import shutil
import re
from collections import Counter

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from extract import extract_text
from summarize import summarize_text

# --- helper: keywords ---
def extract_keywords(text, top_n=10):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set([
        "the","and","is","in","to","of","a","for","with","on",
        "as","by","an","from","that","this","are","be","it","its"
    ])
    words = [w for w in words if w not in stopwords]
    most_common = Counter(words).most_common(top_n)
    return [word for word, _ in most_common]

# --- load env ---
load_dotenv()

# --- app & CORS ---
app = FastAPI(title="Document Summarizer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- determine absolute paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(BASE_DIR, "frontend")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- serve static files under /static ---
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# --- serve index.html at / ---
@app.get("/")
async def home():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to the Document Summarizer API. Go to /docs or /static/index.html to open the UI."}

# --- upload endpoint (unchanged core logic) ---
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    summary_length: str = Form("medium")
):
    try:
        # save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # extract & summarize
        text = extract_text(file_path)
        summary = summarize_text(text, length=summary_length)
        keywords = extract_keywords(summary, top_n=15)

        # clean up
        os.remove(file_path)

        return {
            "filename": file.filename,
            "extracted_text": text[:1000],
            "summary": summary,
            "keywords": keywords
        }
    except Exception as e:
        return {"error": str(e)}
# --- run (Hugging Face compatible) ---
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))  # HF will set PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)

