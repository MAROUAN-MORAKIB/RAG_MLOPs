import os, shutil,threading
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

INDEX_DIR = os.getenv("INDEX_DIR", "/app/data/indexes")

def index_path(hash_id: str) -> str:
    return os.path.join(INDEX_DIR, f"faiss_{hash_id}")

def save_faiss_async(vs: FAISS, path: str):
    def _save():
        vs.save_local(path)
    t = threading.Thread(target=_save, daemon=True)
    t.start()

def load_faiss(embeddings, hash_id: str):
    index_dir = os.getenv("INDEX_DIR", "/app/data/indexes")
    path = os.path.join(index_dir, hash_id)
    if not os.path.exists(path):
        return None
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)


def build_faiss(texts: list[Document], embeddings) -> FAISS:
    return FAISS.from_documents(texts, embeddings)
