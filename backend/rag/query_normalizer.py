import re


class QueryNormalizer:
    """
    Cleans and normalizes user queries before retrieval.
    """

    @staticmethod
    def normalize(query: str) -> str:

        query = query.lower().strip()

        # Remove punctuation
        query = re.sub(r"[^\w\s]", " ", query)

        # Remove common filler phrases
        fillers = [
            "tell me about",
            "can you tell me about",
            "can you explain",
            "please explain",
            "explain",
            "show me",
            "give me",
            "i want to know about",
            "i want to know",
            "what can you tell me about",
            "could you tell me about",
            "please tell me about",
            "do you have",
            "information about",
            "details about",
        ]

        for phrase in fillers:
            query = query.replace(phrase, "")

        # Remove extra spaces
        query = re.sub(r"\s+", " ", query).strip()

        return query