from backend.rag.retriever import Retriever
from backend.rag.bm25 import BM25Retriever
from backend.rag.rrf import ReciprocalRankFusion
from backend.config.settings import TOP_K

import time


class HybridSearch:
    """
    Hybrid Retrieval Pipeline

        Semantic Search
              +
         BM25 Search
              +
    Reciprocal Rank Fusion
    """

    def __init__(self):

        print("\n========== Initializing Hybrid Search ==========\n")

        init_start = time.perf_counter()

        self.vector_retriever = Retriever()

        self.bm25 = BM25Retriever()
        self.bm25.load()

        print(f"HybridSearch Initialization : {time.perf_counter() - init_start:.3f} sec\n")

    def search(self, query: str):

        print("\n================ HYBRID SEARCH ================\n")
        print(f"Query : {query}\n")

        total_start = time.perf_counter()

        # -------------------------------------------------
        # Semantic Search
        # -------------------------------------------------

        semantic_start = time.perf_counter()

        try:
            semantic_results = self.vector_retriever.search(query)

            semantic_time = time.perf_counter() - semantic_start

            print(f"Semantic Search : {semantic_time:.3f} sec")
            print(f"Semantic Results : {len(semantic_results)}")

        except Exception as e:

            print(f"Semantic Search Error : {e}")

            semantic_results = []

        print()

        # -------------------------------------------------
        # BM25 Search
        # -------------------------------------------------

        bm25_start = time.perf_counter()

        try:

            bm25_results = self.bm25.search(
                query=query,
                top_k=TOP_K
            )

            bm25_time = time.perf_counter() - bm25_start

            print(f"BM25 Search : {bm25_time:.3f} sec")
            print(f"BM25 Results : {len(bm25_results)}")

        except Exception as e:

            print(f"BM25 Error : {e}")

            bm25_results = []

        print()

        # -------------------------------------------------
        # Reciprocal Rank Fusion
        # -------------------------------------------------

        rrf_start = time.perf_counter()

        try:

            final_results = ReciprocalRankFusion.fuse(
                semantic_results,
                bm25_results
            )

            rrf_time = time.perf_counter() - rrf_start

            print(f"RRF Fusion : {rrf_time:.3f} sec")
            print(f"Final Results : {len(final_results)}")

        except Exception as e:

            print(f"RRF Error : {e}")

            final_results = []

        print()

        # -------------------------------------------------
        # Total Time
        # -------------------------------------------------

        total_time = time.perf_counter() - total_start

        print("===============================================")
        print(f"Total Hybrid Search Time : {total_time:.3f} sec")
        print("===============================================\n")

        return final_results