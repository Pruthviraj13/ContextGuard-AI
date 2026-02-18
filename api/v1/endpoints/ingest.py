from fastapi import APIRouter, UploadFile
from app.vectorstore.chunking import chunk_text
from app.vectorstore.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FaissStore

router = APIRouter()

embedder = EmbeddingModel()
store = FaissStore(dim=384)

@router.post("/")
async def ingest_document(file: UploadFile):
    text = (await file.read()).decode()
    chunks = chunk_text(text)

    vectors = embedder.embed(chunks)
    metadatas = [{"text": c, "source": file.filename} for c in chunks]

    store.add(vectors, metadatas)

    return {"chunks_ingested": len(chunks)}
