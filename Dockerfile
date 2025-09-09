# Use slim Python image
FROM python:3.11-slim

# Install system deps (tesseract + build deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (speeds rebuild)
COPY requirements.txt .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Ensure frontend is present
# Expose port (Render will set $PORT env var)
EXPOSE 8000

# Start uvicorn. Render will set PORT in environment.
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
