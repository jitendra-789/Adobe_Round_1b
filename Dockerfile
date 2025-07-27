# Base Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies (use offline cache if you have one)
RUN pip install --no-cache-dir -r requirements.txt

# Avoid internet usage during container runtime
ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1
ENV HF_HUB_OFFLINE=1

# Ensure models and tokenizers are available locally
# Assumes your `models/` directory already has the necessary model files
RUN ls models

# Default command
CMD ["python", "main.py"]