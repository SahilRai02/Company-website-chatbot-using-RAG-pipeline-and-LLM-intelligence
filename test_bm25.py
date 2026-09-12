from backend.rag.bm25 import BM25Retriever

bm25 = BM25Retriever()
bm25.load()

results = bm25.search(
    "What ERP services does Navsoft provide?"
)

for i, result in enumerate(results, start=1):

    print("=" * 80)
    print(f"Result {i}")
    print("=" * 80)

    print("Score :", result["score"])
    print("Source :", result["metadata"]["source"])
    print()

    print(result["text"][:400])