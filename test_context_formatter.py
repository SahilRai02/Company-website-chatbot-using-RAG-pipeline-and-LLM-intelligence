from backend.rag.hybrid_search import HybridSearch
from backend.rag.reranker import CrossEncoderReranker
from backend.rag.context_formatter import ContextFormatter


query = "What ERP services does Navsoft provide?"

hybrid = HybridSearch()

results = hybrid.search(query)

results = CrossEncoderReranker.rerank(
    query=query,
    retrieved_chunks=results
)

context = ContextFormatter.format(results)

print(context)