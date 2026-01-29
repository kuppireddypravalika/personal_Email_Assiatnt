from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from app.config import settings

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBED_MODEL)

    def embed(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, settings.EMBED_DIM))
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
