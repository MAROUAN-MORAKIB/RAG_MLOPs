import hashlib, tempfile, os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def file_md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

def load_pdf_bytes(file_bytes: bytes) -> list:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        path = tmp.name
    try:
        docs = PyPDFLoader(path).load()
        return docs
    finally:
        if os.path.exists(path):
            os.remove(path)

def split_docs(docs, chunk_size=1500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    # Filter tiny/blank chunks
    return [c for c in chunks if c.page_content and len(c.page_content.strip()) > 30]
