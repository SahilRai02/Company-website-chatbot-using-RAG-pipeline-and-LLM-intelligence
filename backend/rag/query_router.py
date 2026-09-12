class QueryRouter:
    """
    Routes user queries before RAG execution.
    """

    GREETINGS = {
        "hi",
        "hello",
        "hey",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    }

    THANKS = {
        "thanks",
        "thank you",
        "thx"
    }

    GOODBYE = {
        "bye",
        "goodbye",
        "see you"
    }

    @classmethod
    def classify(cls, query: str):

        text = query.strip().lower()

        if text in cls.GREETINGS:
            return "greeting"

        if text in cls.THANKS:
            return "thanks"

        if text in cls.GOODBYE:
            return "goodbye"

        return "knowledge"