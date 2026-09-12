from google import genai

from backend.config.settings import (
    GOOGLE_API_KEY,
    LLM_MODEL,
)


class GeminiClient:

    def __init__(self):
        print("API KEY:", GOOGLE_API_KEY[:10] + "...")
        print("MODEL:", LLM_MODEL)

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        response = self.client.models.generate_content(
            model=LLM_MODEL,
            contents=[
                system_prompt,
                user_prompt
            ]
        )

        return response.text

    def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        stream = self.client.models.generate_content_stream(
            model=LLM_MODEL,
            contents=[
                system_prompt,
                user_prompt
            ]
        )

        for chunk in stream:

            if chunk.text:

                yield chunk.text