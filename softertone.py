
import google.generativeai as genai
import geminikey

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.cloud import language_v1

# Define the scopes for the OAuth 2.0 flow
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Initialize the OAuth 2.0 flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret_714150796131-a2lqseh1uibg7c258ug2tt9t3pg62g4o.apps.googleusercontent.com.json', scopes=SCOPES)

# Start the OAuth 2.0 flow to obtain user consent and generate credentials
credentials = flow.run_local_server(port=0)
# Initialize Google Cloud Natural Language client with the obtained credentials
language_client = language_v1.LanguageServiceClient(credentials=credentials)

# API KEY
GOOGLE_API_KEY = geminikey.key
genai.configure(api_key=GOOGLE_API_KEY)

# Initializing the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Starting a chat session
chat = model.start_chat(history=[])

# Questions and answers format
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

# Scoring rules
scoring = {
    'positive': 0,
    'negative': 1
}

# Recording user responses and calculating score
total_score = 0
for i, question in enumerate(questions):

    # Let Gemini rephrase the question
    response = chat.send_message("rephrase the question in a softer tone, avoiding direct references to physical observations or limitations: "+question)
    rephrased_question = response.text

    print("Gemini:", rephrased_question)
    user_input = input("User: ").strip()

    # Perform sentiment analysis on user's response
    document = language_v1.Document(content=user_input, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment

    # Determine sentiment score
    sentiment_score = 'positive' if sentiment.score >= 0 else 'negative'

    # Adjust scoring based on sentiment for questions 1-9
    if i < 9:
        total_score += scoring[sentiment_score]
    else:
        # For question 10, sentiment score is reversed
        total_score += 1 if sentiment_score == 'positive' else 0

print("Total Q-CHAT-10 Score:", total_score)
if total_score >= 3:
    print("The health professional may consider referring your child for a multi-disciplinary assessment.")