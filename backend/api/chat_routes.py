from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.concurrency import iterate_in_threadpool
from pydantic import BaseModel

from backend.services.chat_pipeline import ChatPipeline



router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


pipeline = ChatPipeline()


class ChatRequest(BaseModel):
    query: str


@router.post("/")
async def chat(request: ChatRequest):

    result = pipeline.chat(
        request.query
    )

    return {
        "status": "success",
        "answer": result["answer"],
        "sources": result["sources"],
        "context_chunks": result["context_chunks"]
    }

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
         iterate_in_threadpool(
            pipeline.stream_chat(request.query)
        ),
        media_type="text/plain; charset=utf-8"
    )