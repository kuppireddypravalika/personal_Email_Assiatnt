import os
import json
import faiss
import numpy as np


class FaissStore:

    def __init__(self, user_id: str, dim: int = 384):
        self.user_id = user_id
        self.dim = dim

        
        self.user_dir = os.path.join("data", "faiss", user_id)
        os.makedirs(self.user_dir, exist_ok=True)

        self.index_path = os.path.join(self.user_dir, "index.faiss")
        self.meta_path = os.path.join(self.user_dir, "meta.json")

        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

       
        if os.path.exists(self.meta_path):
            try:
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
            except Exception:
                self.metadata = []
        else:
            self.metadata = []

       
        self.existing_ids = {
            m.get("message_id") for m in self.metadata
        }

    def add(self, vectors, metas):
        if vectors is None or len(vectors) == 0:
            return

        vectors = np.array(vectors, dtype="float32")
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        self.index.add(vectors)
        self.metadata.extend(metas)
        self._save()

    def search(self, query_vector, top_k: int = 5):
        if self.index.ntotal == 0:
            return []

        query_vector = np.array(query_vector, dtype="float32")
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        _, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
