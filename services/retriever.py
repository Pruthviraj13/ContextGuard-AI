from app.vectorstore.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FaissStore

class Retriever:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.store = FaissStore(dim=384)

    def retrieve(self, question: str, top_k: int = 5):
        vector = self.embedder.embed([question])
        return self.store.search(vector, top_k)
