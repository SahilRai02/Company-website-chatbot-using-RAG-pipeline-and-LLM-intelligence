from backend.memory.conversation_memory import ConversationMemory

memory = ConversationMemory()

memory.add_user_message(
    "Hello"
)

memory.add_assistant_message(
    "Hello, how may I help you?"
)

memory.add_user_message(
    "Tell me about ERP."
)

print(memory.get_history())