from pydantic import BaseModel

class IngestRequest(BaseModel):
    file_name: str
    file_b64: str  # base64

class QueryRequest(BaseModel):
    hash_id: str
    question: str
    k: int = 5
    model: str = "deepseek/deepseek-chat"

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

class FeedbackRequest(BaseModel):
    hash_id: str
    question: str
    answer: str
    label: int  # 1=up, 0=down
    comment: str | None = None
