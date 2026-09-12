import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi

from backend.config.settings import BM25_DIR
import time

start = time.perf_counter()


class BM25Retriever:
    """
    BM25 keyword retriever.

    Responsibilities:
    - Build BM25 Index
    - Save Index
    - Load Index
    - Search Documents
    """

    def __init__(self):

        self.index_path = Path(BM25_DIR) / "bm25.pkl"
        self.docs_path = Path(BM25_DIR) / "documents.pkl"

        self.bm25 = None
        self.documents = None

    def build(self, chunks):

        self.documents = chunks

        corpus = [
            chunk["text"].lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(corpus)

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.index_path, "wb") as f:
            pickle.dump(self.bm25, f)

        with open(self.docs_path, "wb") as f:
            pickle.dump(self.documents, f)

    def load(self):

        with open(self.index_path, "rb") as f:
            self.bm25 = pickle.load(f)

        with open(self.docs_path, "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query, top_k=10):

        if self.bm25 is None:
            self.load()

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, chunk in ranked[:top_k]:

            metadata = chunk.copy()

            metadata.pop("text", None)
            metadata.pop("embedding", None)

            results.append(
                {
                    "text": chunk["text"],
                    "metadata": metadata,
                    "score": float(score)
                }
            )

            end = time.perf_counter()

        print(f"BM25 : {end - start:.3f} sec")

        return results
   