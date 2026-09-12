from datetime import datetime


class MetadataBuilder:
    """
    Builds metadata for every chunk.
    """

    @staticmethod
    def build(chunks):

        enriched_chunks = []

        for chunk in chunks:

            metadata = {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "document_type": "company_content",
                "word_count": len(chunk["text"].split()),
                "char_count": len(chunk["text"]),
                "created_at": datetime.utcnow().isoformat(),
                "text": chunk["text"]
            }

            enriched_chunks.append(metadata)

        return enriched_chunks