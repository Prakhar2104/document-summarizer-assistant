# 📄 Document Summarizer Assistant

Upload **PDFs or images** and instantly get clean **summaries with keyword highlights**.  
Built with FastAPI, Hugging Face Transformers, and OCR (Tesseract + PyMuPDF).

🔗 **Live Demo**: [Try on Hugging Face 🚀](https://huggingface.co/spaces/Prakhar2104/document-summarizer)  
💻 **Source Code**: [GitHub Repository](https://github.com/Prakhar2104/document-summarizer-assistant)

---

## ✨ Features
- 📂 Upload PDFs or image files  
- 🔎 Extract text using OCR (for scanned documents)  
- 🤖 Summarize text with Hugging Face Transformers (BART model)  
- 📌 Highlight important keywords dynamically  
- ⬇ Download generated summaries as `.txt`  

---

## ⚙️ Tech Stack
- **Backend**: FastAPI + Uvicorn  
- **ML/NLP**: Hugging Face Transformers (BART)  
- **OCR**: Tesseract + PyMuPDF  
- **Frontend**: HTML, CSS, JavaScript  
- **Deployment**: Hugging Face Spaces  

---

## 🚀 Run Locally
Clone the project and install dependencies:

```bash
git clone https://github.com/Prakhar2104/document-summarizer-assistant.git
cd document-summarizer-assistant

python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate   # On macOS/Linux

pip install -r requirements.txt
