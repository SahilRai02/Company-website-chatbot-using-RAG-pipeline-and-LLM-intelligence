from backend.rag.hybrid_search import HybridSearch

hybrid = HybridSearch()

results = hybrid.search(
    "What ERP services does Navsoft provide?"
)

for index, result in enumerate(results, start=1):

    print("=" * 80)

    print(f"Rank : {index}")

    print("Source :", result["metadata"]["source"])

    print("RRF Score :", result["rrf_score"])

    print()

    print(result["text"][:400])