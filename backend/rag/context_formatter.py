class ContextFormatter:
    """
    Formats retrieved chunks into a clean context
    for Prompt Builder / LLM.
    """

    @staticmethod
    def format(chunks):

        formatted_context = []

        for chunk in chunks:

            source = chunk["metadata"].get(
                "source",
                "Unknown"
            )

            formatted_context.append(
                f"""Source: {source}

{chunk["text"].strip()}
"""
            )

        print("\n================ CONTEXT SENT TO LLM ================\n")
        print("\n\n".join(formatted_context))

        return "\n\n".join(formatted_context)