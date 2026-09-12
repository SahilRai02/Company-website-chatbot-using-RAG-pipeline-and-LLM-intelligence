import re


class DocumentCleaner:
    """
    Cleans raw document text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean the document while preserving its meaning.

        Args:
            text (str): Raw document text.

        Returns:
            str: Cleaned text.
        """

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Trim whitespace
        text = text.strip()

        return text