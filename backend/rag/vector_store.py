import chromadb

from backend.config.settings import (
    CHROMA_DB_DIR,
    COLLECTION_NAME
)


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR)
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def add_documents(self, chunks):

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in chunks:

            ids.append(
                f"{chunk['source']}_{chunk['chunk_id']}"
            )

            documents.append(chunk["text"])

            embeddings.append(
                chunk["embedding"].tolist()
            )

            metadata = chunk.copy()

            metadata.pop("text", None)
            metadata.pop("embedding", None)

            metadatas.append(metadata)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def count(self):

        return self.collection.count()
    
    def search(self, query_embedding, top_k):

        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
    
    def reset_collection(self):

        self.client.delete_collection(
        name=self.collection.name
    )

        self.collection = self.client.get_or_create_collection(
        name=self.collection.name
    )