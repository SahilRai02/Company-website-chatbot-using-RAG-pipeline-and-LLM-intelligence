from backend.rag.loader import DocumentLoader
from backend.rag.cleaner import DocumentCleaner
from backend.rag.chunker import DocumentChunker
from backend.rag.metadata import MetadataBuilder

loader = DocumentLoader()
cleaner = DocumentCleaner()
chunker = DocumentChunker()

documents = loader.load_all_txt()

for name, content in documents.items():

    cleaned = cleaner.clean(content)

    chunks = chunker.chunk_document(name, cleaned)

    metadata = MetadataBuilder.build(chunks)

    print("=" * 80)
    print(name)
    print("=" * 80)

    print(metadata[0])

    from backend.rag.embedding_provider import EmbeddingProvider

texts = [
    chunk["text"]
    for chunk in metadata
]

embeddings = EmbeddingProvider.embed_documents(texts)

print("\nEmbedding Shape:")
print(embeddings.shape)

from backend.rag.vector_store import VectorStore

chunks = EmbeddingProvider.attach_embeddings(metadata)

db = VectorStore()

db.add_documents(chunks)

print("\nStored Chunks :", db.count())