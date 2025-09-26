FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for FAISS + psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code (no .env here for security!)
COPY app/ app/
COPY configs/ configs/
COPY data/ data/

EXPOSE 8000

# Start API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
