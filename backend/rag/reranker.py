import torch
from sentence_transformers import CrossEncoder

from backend.config.settings import (
    RERANKER_MODEL,
    FINAL_TOP_K,
    RERANK_THRESHOLD
)


class CrossEncoderReranker:
    """
    Cross Encoder Reranker

    Responsibilities
    ----------------
    - Load Cross Encoder Model
    - Score Retrieved Chunks
    - Return Best FINAL_TOP_K Chunks
    """

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(f"\nLoading Reranker : {RERANKER_MODEL}\n")

            

            device = "cuda" if torch.cuda.is_available() else "cpu"

            print(f"Reranker Device : {device}")

            cls._model = CrossEncoder(
                RERANKER_MODEL,
                device=device
            )

            print("Reranker Loaded Successfully.\n")

        return cls._model

    @classmethod
    def rerank(
        cls,
        query: str,
        retrieved_chunks: list
    ):

        model = cls.get_model()

        sentence_pairs = [
            (query, chunk["text"])
            for chunk in retrieved_chunks
        ]

        scores = model.predict(sentence_pairs)

        for chunk, score in zip(retrieved_chunks, scores):

            chunk["rerank_score"] = float(score)

        reranked = sorted(
            retrieved_chunks,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:FINAL_TOP_K]