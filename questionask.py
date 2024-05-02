import os
import google.generativeai as genai
import geminikey

# API KEY
GOOGLE_API_KEY = geminikey.key
genai.configure(api_key=GOOGLE_API_KEY)

# Initializing the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Starting a chat session
chat = model.start_chat(history=[])

# Questions for Q-CHAT-10
questions = [
    "Does your child look at you when you call his/her name?",
    "How easy is it for you to get eye contact with your child?",
    "Does your child point to indicate that s/he wants something (e.g., a toy that is out of reach)?",
    "Does your child point to share interest with you (e.g., pointing at an interesting sight)?",
    "Does your child pretend (e.g., care for dolls, talk on a toy phone)?",
    "Does your child follow where you’re looking?",
    "If you or someone else in the family is visibly upset, does your child show signs of wanting to comfort them (e.g., stroking hair, hugging them)?",
    "Would you describe your child’s first words as:",
    "Does your child use simple gestures (e.g., wave goodbye)?",
    "Does your child stare at nothing with no apparent purpose?"
]

# Responses storage
user_responses = []

for question in questions:
    # Sending the question to the user
    print("Chatbot: ", question)
    
    # Getting user response
    user_input = input("User: ")
    
    # Recording user response
    user_responses.append(user_input)

# Presenting all user responses at the end
print("All Responses:")
for i, response in enumerate(user_responses, start=1):
    print(f"Question {i}: {response}")
