from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class DocumentChunker:
    """
    Splits cleaned documents into overlapping chunks.
    """

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                ""
            ]
        )

    def chunk_document(self, document_name: str, text: str):

        chunks = self.splitter.split_text(text)

        chunk_list = []

        for index, chunk in enumerate(chunks, start=1):

            chunk_list.append(
                {
                    "chunk_id": index,
                    "source": document_name,
                    "text": chunk
                }
            )

        return chunk_list