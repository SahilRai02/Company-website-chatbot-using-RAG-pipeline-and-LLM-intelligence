from backend.rag.hybrid_search import HybridSearch
from backend.rag.reranker import CrossEncoderReranker
from backend.rag.context_formatter import ContextFormatter
from backend.rag.prompt_builder import PromptBuilder


query = "What ERP services does Navsoft provide?"

hybrid = HybridSearch()

results = hybrid.search(query)

results = CrossEncoderReranker.rerank(
    query=query,
    retrieved_chunks=results
)

context = ContextFormatter.format(results)

prompt = PromptBuilder.build(
    query=query,
    context=context
)

print("=" * 80)
print("SYSTEM PROMPT")
print("=" * 80)
print(prompt["system_prompt"])

print()

print("=" * 80)
print("USER PROMPT")
print("=" * 80)
print(prompt["user_prompt"])