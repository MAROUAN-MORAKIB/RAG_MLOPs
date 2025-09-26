import base64, os, time
from fastapi import FastAPI, HTTPException, Response
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.schemas import IngestRequest, QueryRequest, QueryResponse, FeedbackRequest
from app.ingest import ingest_pdf
from app.deps import get_embeddings
from app.vectorstore import load_faiss
from app.rag_engine import build_context, answer_with_context
from app.feedback import init_feedback_table, add_feedback
from app.telemetry import (
    REQUEST_COUNTER,
    REQUEST_LATENCY,
    TOKENS_USED,
    CHUNKS_RETRIEVED,
)

load_dotenv()

app = FastAPI(title="RAG MLOps API")


@app.on_event("startup")
def _init():
    init_feedback_table()
    os.makedirs(os.getenv("INDEX_DIR", "/app/data/indexes"), exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post("/ingest")
def ingest(req: IngestRequest):
    with REQUEST_LATENCY.labels(endpoint="/ingest").time():
        try:
            file_bytes = base64.b64decode(req.file_b64)
            hash_id = ingest_pdf(req.file_name, file_bytes)
            REQUEST_COUNTER.labels(endpoint="/ingest", status=200).inc()
            return {"hash_id": hash_id}
        except Exception as e:
            REQUEST_COUNTER.labels(endpoint="/ingest", status=500).inc()
            raise HTTPException(500, f"Ingestion error: {e}")


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    with REQUEST_LATENCY.labels(endpoint="/query").time():
        try:
            vs = load_faiss(get_embeddings(), req.hash_id)
            
            if vs is None:
                raise HTTPException(status_code=404, detail=f"Index {req.hash_id} not found or still processing")

            retriever = vs.as_retriever(search_kwargs={"k": req.k})
            docs = retriever.get_relevant_documents(req.question)

            # Track how many chunks were retrieved
            CHUNKS_RETRIEVED.labels(endpoint="/query").observe(len(docs))

            # Build context
            context, sources = build_context(docs)

            # Call LLM
            answer = answer_with_context(req.model, context, req.question)

            # Estimate tokens (rough)
            token_count = len(answer.split())
            TOKENS_USED.labels(endpoint="/query").inc(token_count)

            REQUEST_COUNTER.labels(endpoint="/query", status=200).inc()
            return QueryResponse(answer=answer, sources=sources)

        except Exception as e:
            REQUEST_COUNTER.labels(endpoint="/query", status=500).inc()
            raise HTTPException(status_code=500, detail=f"Query error: {e}")


@app.post("/feedback")
def feedback(req: FeedbackRequest):
    with REQUEST_LATENCY.labels(endpoint="/feedback").time():
        try:
            add_feedback(req.hash_id, req.question, req.answer, req.label, req.comment)
            REQUEST_COUNTER.labels(endpoint="/feedback", status=200).inc()
            return {"ok": True}
        except Exception as e:
            REQUEST_COUNTER.labels(endpoint="/feedback", status=500).inc()
            raise HTTPException(status_code=500, detail=f"Feedback error: {e}")
