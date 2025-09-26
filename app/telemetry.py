from prometheus_client import Counter, Histogram

# Existing metrics
REQUEST_COUNTER = Counter(
    "rag_requests_total",
    "Total requests to RAG API",
    ["endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "rag_request_latency_seconds",
    "Request latency (seconds) per endpoint",
    ["endpoint"]
)

# New custom metrics
TOKENS_USED = Counter(
    "rag_tokens_total",
    "Total number of tokens used in responses",
    ["endpoint"]
)

CHUNKS_RETRIEVED = Histogram(
    "rag_chunks_retrieved",
    "Number of chunks retrieved from FAISS per query",
    ["endpoint"]
)
