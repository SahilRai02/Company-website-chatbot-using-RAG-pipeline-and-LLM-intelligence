from groq import Groq
from backend.config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Reply with only: Hello"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)