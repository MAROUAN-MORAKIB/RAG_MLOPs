from app.deps import get_openrouter_client
from typing import Sequence
from langchain.docstore.document import Document

SYSTEM_PROMPT = "You answer questions ONLY using the provided PDF context. If not enough info, say so."

def answer_with_context(model: str, context: str, question: str) -> str:
    client = get_openrouter_client()
    resp = client.chat.completions.create(
        model=model,  # e.g., "deepseek/deepseek-chat"
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return resp.choices[0].message.content

def build_context(docs: Sequence[Document]) -> tuple[str, list[str]]:
    parts, sources = [], []
    for d in docs:
        parts.append(d.page_content)
        p = d.metadata.get("page")
        sources.append(f"p.{p+1}" if isinstance(p, int) else "p.?")
    return "\n\n".join(parts), sorted(set(sources))
