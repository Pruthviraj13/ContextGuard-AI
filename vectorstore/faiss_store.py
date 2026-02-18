import faiss
import pickle
import os

class FaissStore:
    def __init__(self, dim: int, index_path="faiss.index", meta_path="meta.pkl"):
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)

    def add(self, vectors, metadatas):
        self.index.add(vectors)
        self.metadata.extend(metadatas)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, vector, top_k=5):
        distances, indices = self.index.search(vector, top_k)
        return [self.metadata[i] for i in indices[0]]
