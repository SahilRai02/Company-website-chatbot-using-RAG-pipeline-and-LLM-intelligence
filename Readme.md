# Company Website AI Chatbot

An AI-powered company website chatbot built using a Retrieval-Augmented Generation (RAG) pipeline and Large Language Models (LLMs).

The chatbot retrieves relevant information from a knowledge base before generating a response, helping provide context-aware and grounded answers instead of relying only on the language model's internal knowledge.

## Overview

This project implements a complete RAG-based conversational pipeline that combines document retrieval, hybrid search, reranking, conversation memory, and LLM-based response generation.

The system is designed to answer questions using information retrieved from company-related documents while maintaining conversational context.

## Key Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using embeddings
- BM25 keyword-based retrieval
- Hybrid search combining semantic and lexical retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Context-aware prompt construction
- Conversation memory
- Query normalization and routing
- Document cleaning and chunking
- Metadata processing
- LLM-based response generation
- FastAPI backend
- Local Ollama support
- Groq LLM integration
- Google GenAI integration
- ChromaDB vector storage

## RAG Pipeline

```text
User Query
    ↓
Query Normalization / Routing
    ↓
Hybrid Retrieval
    ├── Semantic Search
    └── BM25 Search
            ↓
       RRF Fusion
            ↓
        Reranking
            ↓
    Context Formatting
            ↓
      Prompt Builder
            ↓
           LLM
            ↓
        Response