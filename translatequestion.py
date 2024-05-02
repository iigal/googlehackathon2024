import os
import google.generativeai as genai
import geminikey

# API KEY
GOOGLE_API_KEY = geminikey.key
genai.configure(api_key=GOOGLE_API_KEY)

# Initializing the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Starting a chat session
chat = model.start_chat(history=[], language='es')

while True:
    # Getting user input
    user_input = input("User: ")

    # Exiting the chat if the user types 'exit'
    if user_input.lower() == 'exit':
        break

    # Sending the user's message to the model and getting a response
    response = chat.send_message(user_input, stream=True)

    # Printing the model's response
    for chunk in response:
        if chunk.text:
            print("Chatbot: ", chunk.text)
