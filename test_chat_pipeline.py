from backend.services.chat_pipeline import ChatPipeline

chatbot = ChatPipeline()

while True:

    query = input("\nYou : ")

    if query.lower() in ["exit", "quit"]:

        break

    response = chatbot.chat(query)

    print("\nAssistant:\n")

    print(response)