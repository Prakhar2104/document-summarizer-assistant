# summarize.py
import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()  # load HF_TOKEN from .env

# Initialize Hugging Face summarizer
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    tokenizer="facebook/bart-large-cnn",
    device=-1  # CPU
)

# Map summary length options
SUMMARY_LENGTHS = {
    "short": {"min_length": 50, "max_length": 150},
    "medium": {"min_length": 150, "max_length": 300},
    "long": {"min_length": 300, "max_length": 500},
}

def summarize_text(text, length="medium", max_input_chars=3000):
    """
    Summarize text safely. Handles large text by trimming or chunking.
    length: "short", "medium", "long"
    """
    if not text.strip():
        return "⚠️ No text to summarize."

    # Trim input text if too long
    text = text[:max_input_chars]

    length_params = SUMMARY_LENGTHS.get(length, SUMMARY_LENGTHS["medium"])

    try:
        summary = summarizer(
            text,
            min_length=length_params["min_length"],
            max_length=length_params["max_length"]
        )[0]["summary_text"]
        return summary
    except Exception as e:
        return f"Summarization failed: {str(e)}"
