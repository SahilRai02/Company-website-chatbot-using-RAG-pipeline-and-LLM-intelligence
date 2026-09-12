from backend.rag.hybrid_search import HybridSearch
from backend.rag.reranker import CrossEncoderReranker


hybrid = HybridSearch()

results = hybrid.search(
    "What ERP services does Navsoft provide?"
)

results = CrossEncoderReranker.rerank(
    query="What ERP services does Navsoft provide?",
    retrieved_chunks=results
)

for i, chunk in enumerate(results, start=1):

    print("=" * 80)

    print(f"Rank : {i}")

    print("Score :", round(chunk["rerank_score"], 4))

    print("Source :", chunk["metadata"]["source"])

    print()

    print(chunk["text"][:400])