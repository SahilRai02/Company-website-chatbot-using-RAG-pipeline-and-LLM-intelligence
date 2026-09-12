from groq import Groq

from backend.config.settings import (
    GROQ_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
)


class OllamaClient:
    """
    Wrapper around Groq.

    Responsibilities
    ----------------
    - Connect to Groq
    - Send prompts
    - Return generated response
    """

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        response = self.client.chat.completions.create(

            model=LLM_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ],

            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,

        )

        return response.choices[0].message.content

    def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        stream = self.client.chat.completions.create(

            model=LLM_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ],

            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=MAX_TOKENS,

            stream=True

        )

        for chunk in stream:

            if chunk.choices:

                delta = chunk.choices[0].delta

                if delta and delta.content:

                    yield delta.content