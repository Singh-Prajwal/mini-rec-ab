import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class MiniRec:
    def __init__(self, csv_path: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        df = pd.read_csv(csv_path)
        self.ids = df["id"].tolist()
        self.titles = dict(zip(df["id"], df["title"]))
        plots = df["plot"].tolist()
        embeds = self.model.encode(plots, normalize_embeddings=True)
        d = embeds.shape[1]
        self.index = faiss.IndexFlatIP(d)  # cosine (after L2-norm)
        self.index.add(embeds.astype("float32"))

    def recommend(self, text: str, k: int = 3, metric="cosine"):
        query_vec = self.model.encode([text], normalize_embeddings=True)
        scores, idxs = self.index.search(query_vec.astype("float32"), k)
        rec_ids = [self.ids[i] for i in idxs[0]]
        return [{"id": i, "title": self.titles[i], "score": float(s)} 
                for i, s in zip(rec_ids, scores[0])]