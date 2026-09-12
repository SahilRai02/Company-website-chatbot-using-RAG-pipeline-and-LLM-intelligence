import re


class PersonaProcessor:
    """
    Processes the raw persona document before
    it is sent to the Prompt Builder.

    Responsibilities
    ----------------
    - Remove BOM characters
    - Normalize whitespace
    - Remove excessive blank lines
    - Keep original content intact
    """

    @staticmethod
    def process(persona: str) -> str:

        # Remove UTF-8 BOM
        persona = persona.replace("\ufeff", "")

        # Normalize line endings
        persona = persona.replace("\r\n", "\n")

        # Remove trailing spaces
        persona = "\n".join(
            line.strip()
            for line in persona.splitlines()
        )

        # Remove multiple blank lines
        persona = re.sub(
            r"\n{3,}",
            "\n\n",
            persona
        )

        return persona.strip()