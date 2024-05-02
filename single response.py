import google.generativeai as genai
import geminikey

# Configure the API with your key
GOOGLE_API_KEY = geminikey.key
genai.configure(api_key=GOOGLE_API_KEY)

# Start a chat session
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Send a message and get a response
prompt = "write top 10 words that is most frequently used ?"
response = chat.send_message(prompt, stream=True)
for chunk in response:
    if chunk.text:
        print(chunk.text)
