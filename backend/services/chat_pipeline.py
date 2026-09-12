from backend.memory.conversation_memory import ConversationMemory
from backend.rag.hybrid_search import HybridSearch
from backend.rag.reranker import CrossEncoderReranker
from backend.rag.context_formatter import ContextFormatter
from backend.rag.prompt_builder import PromptBuilder
from backend.llm.ollama_client import OllamaClient
from backend.rag.query_router import QueryRouter
from backend.config.settings import RERANK_THRESHOLD
from backend.rag.query_normalizer import QueryNormalizer


import time


class ChatPipeline:
    """
    End-to-End Chat Pipeline.

    Responsibilities
    ----------------
    - Maintain conversation memory
    - Retrieve relevant knowledge
    - Rerank retrieved documents
    - Build context
    - Build prompts
    - Generate LLM response
    """

    def __init__(self):

        self.memory = ConversationMemory()
        self.hybrid = HybridSearch()
        self.llm = OllamaClient()
    def _retrieve_context(self, query: str):
        """
        Shared RAG pipeline.

        Returns:
            prompts,
            sources,
            reranked_chunks,
            profiling
        """

        pipeline_start = time.perf_counter()

        # -----------------------------
        # Add User Message
        # -----------------------------
        self.memory.add_user_message(query)
        memory_time = time.perf_counter()

        # -----------------------------
        # Hybrid Retrieval
        # -----------------------------
        retrieve_start = time.perf_counter()

        retrieved_chunks = self.hybrid.search(query)

        

        retrieve_time = time.perf_counter()

        # -----------------------------
        # Cross Encoder
        # -----------------------------
        rerank_start = time.perf_counter()

        reranked_chunks = CrossEncoderReranker.rerank(
            query=query,
            retrieved_chunks=retrieved_chunks
        )
        

        rerank_time = time.perf_counter()

        # -----------------------------
        # Context
        # -----------------------------
        context_start = time.perf_counter()

        context = ContextFormatter.format(
            reranked_chunks
        )
        

        context_time = time.perf_counter()

        

       

        prompt_time = time.perf_counter()

        sources = sorted({
            chunk["metadata"]["source"]
            for chunk in reranked_chunks
        })

        profiling = {
            "pipeline_start": pipeline_start,
            "memory_time": memory_time,
            "retrieve_start": retrieve_start,
            "retrieve_time": retrieve_time,
            "rerank_start": rerank_start,
            "rerank_time": rerank_time,
            "context_start": context_start,
            "context_time": context_time,
        }

        return context, sources, reranked_chunks, profiling
    
    def _build_prompt(
        self,
        query: str,
        context: str
    ):

        history = self.memory.get_history()

        prompt_start = time.perf_counter()

        prompts = PromptBuilder.build(
            query=query,
            context=context,
            history=history
        )

        prompt_time = time.perf_counter()

        return prompts, prompt_start, prompt_time
    
    

    def chat(self, query: str):

        pipeline_start = time.perf_counter()
        query = QueryNormalizer.normalize(query)
        expanded_query = QueryExpander.expand(query)

        print("\nExpanded Query :", expanded_query)

        # -----------------------------
        # Query Routing
        # -----------------------------
        intent = QueryRouter.classify(query)

        if intent == "greeting":

            response = """
# Welcome to NAVSOFT AI Assistant!

Hello! I'm here to help you with information about NAVSOFT.

You can ask me about:

- Products & Services
- AWS Solutions
- Healthcare IT
- AI Solutions
- Retail Solutions
- Company Information

How can I assist you today?
"""

            return {
                "answer": response.strip(),
                "sources": [],
                "context_chunks": 0
            }

        if intent == "thanks":

            return {
                "answer": "You're welcome! 😊 Feel free to ask if you need any information about NAVSOFT.",
                "sources": [],
                "context_chunks": 0
            }

        if intent == "goodbye":

            return {
                "answer": "Goodbye! 👋 Have a great day. Feel free to chat with me anytime.",
                "sources": [],
                "context_chunks": 0
            }

        context, sources, reranked_chunks, profiling = self._retrieve_context(
            query
        )

        prompts, prompt_start, prompt_time = self._build_prompt(
            query=query,
            context=context
        )

        profiling["prompt_start"] = prompt_start
        profiling["prompt_time"] = prompt_time

                # -----------------------------
        # Confidence Guardrail
        # -----------------------------
        if (
            not reranked_chunks
            or reranked_chunks[0]["rerank_score"] < RERANK_THRESHOLD
        ):

            return {
                "answer": (
                    f"Sorry, I couldn't find information related to "
                    f"'{query}' in the current Knowledge Base."
                ),
                "sources": [],
                "context_chunks": 0
            }

       

        # -----------------------------
        # LLM Response
        # -----------------------------
        llm_start = time.perf_counter()



        response = self.llm.generate(
            system_prompt=prompts["system_prompt"],
            user_prompt=prompts["user_prompt"]
        )

        llm_time = time.perf_counter()

        # -----------------------------
        # Store Assistant Response
        # -----------------------------
        self.memory.add_assistant_message(response)



        # -----------------------------
        # Profiling
        # -----------------------------
        print("\n==============================")
        print("NAVSOFT RAG Profiling")
        print("==============================")
        print(f"Memory           : {profiling['memory_time'] - profiling['pipeline_start']:.3f} sec")
        print(f"Hybrid Search    : {profiling['retrieve_time'] - profiling['retrieve_start']:.3f} sec")
        print(f"Cross Encoder    : {profiling['rerank_time'] - profiling['rerank_start']:.3f} sec")
        print(f"Context Builder  : {profiling['context_time'] - profiling['context_start']:.3f} sec")
        print(f"Prompt Builder   : {profiling['prompt_time'] - profiling['prompt_start']:.3f} sec")
        print(f"LLM              : {llm_time - llm_start:.3f} sec")
        print("------------------------------")
        print(f"TOTAL            : {llm_time - profiling['pipeline_start']:.3f} sec")
        print("==============================\n")


    
    def stream_chat(self, query: str):
        query = QueryNormalizer.normalize(query)
        

        


        # -----------------------------
        # Query Routing
        # -----------------------------
        intent = QueryRouter.classify(query)

        if intent == "greeting":

            yield """
# Welcome to NAVSOFT AI Assistant!

Hello! I'm here to help you with information about NAVSOFT.

You can ask me about:

- Products & Services
- AWS Solutions
- Healthcare IT
- AI Solutions
- Retail Solutions
- Company Information

How can I assist you today?
""".strip()

            return

        if intent == "thanks":
            yield "You're welcome! 😊 Feel free to ask if you need any information about NAVSOFT."
            return

        if intent == "goodbye":
            yield "Goodbye! 👋 Have a great day. Feel free to chat with me anytime."
            return
        
        yield "__QUERY__\n"
        


        context, sources, reranked_chunks, profiling = self._retrieve_context(
            query
        )
        yield "__SEARCH_DONE__\n"

        prompts, prompt_start, prompt_time = self._build_prompt(
            query=query,
            context=context
        )
        yield "__PROMPT_DONE__\n"

        profiling["prompt_start"] = prompt_start
        profiling["prompt_time"] = prompt_time
        if reranked_chunks:
             print("Top Score :", reranked_chunks[0]["rerank_score"])

                # -----------------------------
        # Confidence Guardrail
        # -----------------------------
        if (
            not reranked_chunks
            or reranked_chunks[0]["rerank_score"] < RERANK_THRESHOLD
        ):

            yield (
                f"Sorry, I couldn't find information related to "
                f"'{query}' in the current Knowledge Base."
            )

            return

        full_response = ""
        print("STREAM_CHAT CALLED")
        yield "__LLM_START__\n"
        for chunk in self.llm.stream_generate(
            system_prompt=prompts["system_prompt"],
            user_prompt=prompts["user_prompt"]
        ):
            print("CHUNK:", repr(chunk))
            full_response += chunk

            yield chunk



            print("\n==============================")
            print("NAVSOFT RAG Profiling")
            print("==============================")
            print(f"Memory           : {profiling['memory_time'] - profiling['pipeline_start']:.3f} sec")
            print(f"Hybrid Search    : {profiling['retrieve_time'] - profiling['retrieve_start']:.3f} sec")
            print(f"Cross Encoder    : {profiling['rerank_time'] - profiling['rerank_start']:.3f} sec")
            print(f"Context Builder  : {profiling['context_time'] - profiling['context_start']:.3f} sec")
            print(f"Prompt Builder   : {profiling['prompt_time'] - profiling['prompt_start']:.3f} sec")
            print("==============================")

        # -----------------------------
        # Save Assistant Message
        # -----------------------------
        self.memory.add_assistant_message(full_response)