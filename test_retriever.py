from backend.rag.retriever import Retriever

retriever = Retriever()

results = retriever.search(
    "What ERP services does Navsoft provide?"
)

print("=" * 80)

for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")
    print("-" * 80)

    print("Score :", result["score"])
    print("Source :", result["metadata"]["source"])
    print()

    print(result["text"][:500])