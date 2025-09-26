# ===============================
# Base image (core dependencies only)
# ===============================
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

# Install core Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (no .env for security)
COPY app/ app/
COPY ops/ ops/

# ===============================
# Full ML image (adds heavy ML libs)
# ===============================
FROM base AS ml

# Install ML dependencies (torch, transformers, faiss, etc.)
COPY requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

# ===============================
# Default run command
# ===============================
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
