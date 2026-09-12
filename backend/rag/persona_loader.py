from backend.rag.loader import DocumentLoader
from backend.rag.persona_processor import PersonaProcessor


class PersonaLoader:
    """
    Loads and processes the assistant persona.
    The persona is loaded only once during the
    application lifetime.
    """

    _persona = None

    @classmethod
    def load(cls):

        if cls._persona is None:

            loader = DocumentLoader()

            raw_persona = loader.load_txt(
                "sandeep_personality.txt"
            )

            cls._persona = PersonaProcessor.process(
                raw_persona
            )

            print("Persona Loaded Successfully.\n")

        return cls._persona