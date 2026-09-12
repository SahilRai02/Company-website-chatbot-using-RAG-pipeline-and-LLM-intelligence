from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"




BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploaded_docs"

PROCESSED_DIR = DATA_DIR / "processed_docs"

CHROMA_DB_DIR = DATA_DIR / "chroma"

BM25_DIR = DATA_DIR / "bm25"

TEMP_DIR = DATA_DIR / "temp"

CACHE_DIR = DATA_DIR / "cache"

DATABASE_DIR = BASE_DIR / "database"

LOG_DIR = BASE_DIR / "logs"




OLLAMA_BASE_URL = "http://localhost:11434"

TEMPERATURE = 0.2

TOP_P = 0.9

MAX_TOKENS = 300
REPEAT_PENALTY = 1.15


EMBEDDING_MODEL = "BAAI/bge-m3"

TOP_K = 10

FINAL_TOP_K = 10

RRF_K = 60

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

APP_NAME = "NAVSOFT Enterprise AI Assistant"

VERSION = "1.0.0"

COLLECTION_NAME = "navsoft_knowledge_base"


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_THRESHOLD = 2.0


MAX_CONTEXT_DOCUMENTS = 5
MAX_HISTORY_MESSAGES = 6

TEMPERATURE = 0.2
TOP_P = 0.9

SYSTEM_NAME = "NAVSOFT AI Assistant"