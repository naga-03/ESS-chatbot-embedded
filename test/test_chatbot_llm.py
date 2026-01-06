from src.chatbot import ESSChatbot

# Test the chatbot with LLM
chatbot = ESSChatbot()

# Test a simple query
response = chatbot.process_message("hello")

print("Response:", response['message'])
print("Success:", response['success'])
print("Intent:", response['intent'])

# Test another query
response2 = chatbot.process_message("What is the leave policy?")
print("\nResponse 2:", response2['message'])
print("Success:", response2['success'])
print("Intent:", response2['intent'])
