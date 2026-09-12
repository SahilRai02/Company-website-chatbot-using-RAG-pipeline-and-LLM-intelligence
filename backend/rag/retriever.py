from backend.rag.embedding_provider import EmbeddingProvider
from backend.rag.vector_store import VectorStore
from backend.config.settings import TOP_K
import time


class Retriever:

    def __init__(self):

        self.vector_store = VectorStore()

    def search(self, query: str):

        embed_start = time.perf_counter()

        query_embedding = EmbeddingProvider.embed_query(query)

        embed_end = time.perf_counter()
        print(f"Embedding : {embed_end - embed_start:.3f} sec")

        


        search_start = time.perf_counter()

        results = self.vector_store.search(
            query_embedding,
            TOP_K
        )

        search_end = time.perf_counter()
        print(f"Chroma Search : {search_end - search_start:.3f} sec")

        

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append(
                {
                    "text": doc,
                    "metadata": meta,
                    "score": round(1 - distance, 4)
                }
            )

        return retrieved_chunks