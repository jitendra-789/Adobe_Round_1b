# Base image with Python 3.10 and CPU-only PyTorch
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY Challenge_1b ./Challenge_1b

# Set environment variables to disable internet
ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1

# Optional: Set model cache path if using pre-downloaded models
ENV TRANSFORMERS_CACHE=/app/Challenge_1b/models

# Set entrypoint (you can modify this based on your actual script)
WORKDIR /app/Challenge_1b
CMD ["python", "main.py"]