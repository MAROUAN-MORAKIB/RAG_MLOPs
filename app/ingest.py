from langchain_community.vectorstores import FAISS
from app.deps import get_embeddings
from app.vectorstore import save_faiss_async  # add this import

def ingest_pdf(file_name: str, file_bytes: bytes) -> str:
    import tempfile, os, hashlib
    from langchain.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(file_bytes)
        temp_path = f.name

    try:
        loader = PyPDFLoader(temp_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        embeddings = get_embeddings()  # your HuggingFaceEmbeddings
        texts_content = [doc.page_content for doc in texts]

        # ⚡ Batch embedding
        vectors = embeddings.embed_documents(texts_content)

        # Build FAISS index directly
        vs = FAISS.from_embeddings(
            [(texts[i].page_content, vectors[i]) for i in range(len(texts))],
            embeddings
        )

        # Save under a hash name
        hash_id = hashlib.sha256(file_bytes).hexdigest()[:16]
        save_path = os.path.join(os.getenv("INDEX_DIR", "/app/data/indexes"), hash_id)
        save_faiss_async(vs, save_path)

        return hash_id
    finally:
        os.remove(temp_path)
