import os

HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN:
    print("Hugging Face token loaded successfully!")
else:
    print("Token not found. Did you set HF_TOKEN?")
