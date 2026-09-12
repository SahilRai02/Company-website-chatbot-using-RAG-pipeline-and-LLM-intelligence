from sentence_transformers import SentenceTransformer
import torch

from backend.config.settings import EMBEDDING_MODEL


class EmbeddingProvider:
    """
    Singleton embedding model provider.
    """

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(f"\nLoading Embedding Model : {EMBEDDING_MODEL}\n")

            device = "cuda" if torch.cuda.is_available() else "cpu"

            print(f"Embedding Device : {device}")

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL,
                trust_remote_code=True,
                device=device
            )

            print("Embedding Model Loaded Successfully.\n")

        return cls._model

    @classmethod
    def embed_documents(cls, texts):

        model = cls.get_model()

        return model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True
        )

    @classmethod
    def embed_query(cls, query):

        model = cls.get_model()

        return model.encode(
            query,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

    @classmethod
    def attach_embeddings(cls, chunks):

        texts = [chunk["text"] for chunk in chunks]

        vectors = cls.embed_documents(texts)

        for chunk, vector in zip(chunks, vectors):
            chunk["embedding"] = vector

        return chunks