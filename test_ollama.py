from backend.llm.ollama_client import OllamaClient

llm = OllamaClient()

response = llm.generate(

    system_prompt="""
You are a helpful AI assistant.
""",

    user_prompt="""
Say hello in one sentence.
"""
)

print(response)