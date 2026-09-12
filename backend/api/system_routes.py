from fastapi import APIRouter
from backend.config.settings import (
    APP_NAME,
    VERSION,
    LLM_MODEL,
    EMBEDDING_MODEL
)

router = APIRouter(
    prefix="/system",
    tags=["System"]
)


@router.get("/status")
async def get_system_status():

    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "Running",
        "llm": LLM_MODEL,
        "embedding": EMBEDDING_MODEL,
        "vector_db": "ChromaDB",
        "retrieval": "Hybrid Search",
        "reranker": "Cross Encoder"
    }