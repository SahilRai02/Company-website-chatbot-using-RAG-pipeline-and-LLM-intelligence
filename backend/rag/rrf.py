from collections import defaultdict

from backend.config.settings import (
    RRF_K,
    FINAL_TOP_K
)


class ReciprocalRankFusion:
    """
    Combines multiple ranked retrieval results
    using Reciprocal Rank Fusion (RRF).
    """

    @staticmethod
    def fuse(vector_results, bm25_results):

        scores = defaultdict(float)
        documents = {}

        # Semantic Search Ranking
        for rank, item in enumerate(vector_results, start=1):

            chunk_id = item["metadata"]["chunk_id"]

            scores[chunk_id] += 1 / (RRF_K + rank)

            documents[chunk_id] = item

        # BM25 Ranking
        for rank, item in enumerate(bm25_results, start=1):

            chunk_id = item["metadata"]["chunk_id"]

            scores[chunk_id] += 1 / (RRF_K + rank)

            documents[chunk_id] = item

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        fused_results = []

        for chunk_id, score in ranked:

            document = documents[chunk_id].copy()

            document["rrf_score"] = round(score, 6)

            fused_results.append(document)

        return fused_results