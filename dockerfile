FROM python:3.10.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    curl \
    ca-certificates \
    libsndfile1 \
    libffi-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set TTS cache location 
ENV TTS_HOME=/app/tts_models

# Pre-download TTS model
RUN python - <<EOF
from TTS.api import TTS
print("Downloading TTS model...")
TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)
print("TTS model downloaded successfully.")
EOF

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn (with longer timeout for ML tasks)
CMD ["gunicorn", "-w", "1", "--timeout", "300", "-b", "0.0.0.0:5000", "app:app"]