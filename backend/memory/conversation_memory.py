from collections import deque

from backend.config.settings import MAX_HISTORY_MESSAGES


class ConversationMemory:
    """
    Maintains conversation history.

    Responsibilities
    ----------------
    - Store chat messages
    - Return recent history
    - Clear conversation
    """

    def __init__(self):

        self.messages = deque(
            maxlen=MAX_HISTORY_MESSAGES
        )

    def add_user_message(self, message: str):

        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_assistant_message(self, message: str):

        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def get_history(self):

        history = []

        for msg in self.messages:

            history.append(
                f'{msg["role"].upper()}: {msg["content"]}'
            )

        return "\n".join(history)

    def clear(self):

        self.messages.clear()