# 📘 RAG MLOps API

A production-ready **Retrieval-Augmented Generation (RAG) system** built with **FastAPI, LangChain, FAISS, PostgreSQL, Prometheus, and Grafana**.  
This project is containerized with **Docker** and supports monitoring, feedback storage, and CI/CD.

---

## ✨ Features

- 📄 **PDF ingestion** → split docs into chunks and embed them.  
- 🤖 **Query API** → answer questions using context retrieved from FAISS.  
- 🧩 **LLM support** → integrates with OpenRouter (DeepSeek, GPT, etc.).  
- 📊 **Monitoring** → Prometheus + Grafana dashboards (requests, latency, tokens, chunks retrieved).  
- 🗃 **Feedback loop** → store user feedback in PostgreSQL.  
- 🐳 **Dockerized** → lightweight & ML-ready builds.  
- ⚡ **CI/CD** → GitHub Actions build & push images automatically.

---

## 🏗️ Architecture

```
+-------------+      +-----------+      +-------------+      +-----------+
|   FastAPI   | ---> |   FAISS   | ---> |   OpenRouter| ---> |   LLMs    |
|   (rag-api) |      |  VectorDB |      |   API       |      |           |
+-------------+      +-----------+      +-------------+      +-----------+

   ↑     |                       Monitoring (Prometheus + Grafana)
   |     ↓
 Feedback DB (Postgres)
```

---

## 🐳 Docker Images

Two Docker images are available:

- `marouanmorakib/rag-api:latest` → **Lightweight** (FastAPI + DB + telemetry, no ML libs)  
- `marouanmorakib/rag-api:ml` → **Full RAG** (includes `torch`, `transformers`, `sentence-transformers`, `faiss`, etc.)

---

## 🚀 Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/MAROUAN-MORAKIB/RAG_PROJECT.git
cd RAG_PROJECT
```

### 2. Run with Docker Compose
```bash
docker-compose -f ops/docker-compose.yml up -d
```

This starts:
- `rag-api` (FastAPI service)  
- `rag-db` (Postgres for feedback)  
- `prometheus` (metrics)  
- `grafana` (dashboards)

### 3. Access services
- API → [http://localhost:8000/docs](http://localhost:8000/docs)  
- Prometheus → [http://localhost:9090](http://localhost:9090)  
- Grafana → [http://localhost:3000](http://localhost:3000) (login: `admin/admin`)

---

## 🔑 Environment Variables

Configure in `.env` (not included in repo, use your own):

```ini
# === OpenRouter ===
OPENROUTER_API_KEY=sk-or-xxx
HF_API_KEY=hf_xxx

# === Storage ===
INDEX_DIR=/app/data/indexes
RAW_DIR=/app/data/raw

# === Database ===
DB_URL=postgresql+psycopg2://postgres:root@rag-db:5432/rag_db
```

---

## 📡 API Endpoints

### 📥 Ingest PDF
```bash
POST /ingest
```
Request:
```json
{
  "file_name": "doc.pdf",
  "file_b64": "<base64-encoded-pdf>"
}
```

Response:
```json
{ "hash_id": "297d2f021f5d4aef" }
```

---

### 🔍 Query
```bash
POST /query
```
Request:
```json
{
  "hash_id": "297d2f021f5d4aef",
  "question": "Give me a summary of the paper",
  "k": 5,
  "model": "deepseek/deepseek-chat"
}
```

Response:
```json
{
  "answer": "This paper proposes ...",
  "sources": ["page_2", "page_3"]
}
```

---

### 📊 Metrics
```bash
GET /metrics
```
Prometheus-compatible metrics: requests, latency, token count, chunks retrieved.

---

### 📝 Feedback
```bash
POST /feedback
```
Request:
```json
{
  "hash_id": "297d2f021f5d4aef",
  "question": "What is the main contribution?",
  "answer": "The paper introduces ...",
  "label": "good",
  "comment": "Accurate and concise"
}
```

Response:
```json
{ "ok": true }
```

---

## 📈 Monitoring

- **Prometheus** scrapes `/metrics` from the API.  
- **Grafana** provides dashboards with:
  - Requests per second  
  - Latency (avg, p95)  
  - Tokens used per query  
  - Chunks retrieved  

---

## ⚙️ Development

### Build light image (CI/staging)
```bash
docker build -t rag-api -f ops/Dockerfile .
```

### Build full ML image (local/prod)
```bash
docker build -t rag-api-ml --target ml -f ops/Dockerfile .
```

---

## 🤝 Contributing
PRs are welcome! Please:
1. Fork the repo  
2. Create a feature branch  
3. Open a PR  

---

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
