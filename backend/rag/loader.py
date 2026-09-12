from pathlib import Path
from backend.config.settings import UPLOAD_DIR


class DocumentLoader:
    """
    Loads knowledge base documents from the upload directory.
    Currently supports .txt files.
    """

    def __init__(self):
        self.upload_dir = Path(UPLOAD_DIR)

    def load_txt(self, filename: str) -> str:
        """
        Load a single text file.

        Args:
            filename (str): Name of the text file.

        Returns:
            str: File content.
        """

        file_path = self.upload_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"{filename} not found.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read()

    def load_all_txt(self) -> dict:
        """
        Load every TXT document from upload folder.

        Returns:
            dict
            {
                filename : content
            }
        """

        documents = {}

        txt_files = self.upload_dir.glob("*.txt")

        for file in txt_files:
            documents[file.name] = self.load_txt(file.name)

        return documents