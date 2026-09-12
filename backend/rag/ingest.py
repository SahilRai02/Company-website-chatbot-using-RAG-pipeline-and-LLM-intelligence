from backend.rag.loader import DocumentLoader
from backend.rag.cleaner import DocumentCleaner
from backend.rag.chunker import DocumentChunker
from backend.rag.metadata import MetadataBuilder
from backend.rag.embedding_provider import EmbeddingProvider
from backend.rag.vector_store import VectorStore
from backend.rag.bm25 import BM25Retriever



class KnowledgeIngestion:

    def __init__(self):

        self.loader = DocumentLoader()
        self.cleaner = DocumentCleaner()
        self.chunker = DocumentChunker()
        self.vector_store = VectorStore()
        self.bm25 = BM25Retriever()

    def ingest(self, filename: str):

        print("Resetting Knowledge Base...")

        self.vector_store.reset_collection()

        print(f"\nLoading : {filename}")

        text = self.loader.load_txt(filename)

        print("Cleaning document...")
        cleaned = self.cleaner.clean(text)

        print("Creating chunks...")
        chunks = self.chunker.chunk_document(filename, cleaned)

        print(f"Chunks Created : {len(chunks)}")

        print("Generating metadata...")
        chunks = MetadataBuilder.build(chunks)

        print("Generating embeddings...")
        chunks = EmbeddingProvider.attach_embeddings(chunks)

        print("Saving into ChromaDB...")
        self.vector_store.add_documents(chunks)

        print("Building BM25 Index...")

        self.bm25.build(chunks)

        self.bm25.save()

        print("BM25 Index Saved.")

        print(f"Documents Stored : {self.vector_store.count()}")

        print("\nKnowledge Base Ready.\n")


if __name__ == "__main__":

    pipeline = KnowledgeIngestion()

    pipeline.ingest("navsoft_website_content.txt")