from flask import Flask, render_template, request, redirect, url_for

from google.cloud import language_v1
import google.generativeai as genai
import geminikey

# Initialize Flask app
app = Flask(__name__)

# Initialize Google Cloud Natural Language client
language_client = language_v1.LanguageServiceClient()

# Set up Gemini API key
GOOGLE_API_KEY = geminikey.key
genai.configure(api_key=GOOGLE_API_KEY)

# Initializing the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Define the questions
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

# Initialize chat session
chat = None

# Initialize history of Q&A
history = []

# Route for homepage
@app.route('/')
def homepage():
    return render_template('index.html', history=history)

# Route for starting the chat
@app.route('/start_chat', methods=['GET', 'POST'])
def start_chat():
    global chat
    chat = model.start_chat(history=[])
    return redirect(url_for('next_question'))

# Route for asking the next question
@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
    global chat
    global questions

    if not chat:
        return redirect(url_for('start_chat'))

    if request.method == 'POST':
        # Save the user's answer to the previous question
        user_answer = request.form['answer']
        history.append(("User", user_answer))

    # If all questions have been asked, display the score
    if len(history)/2 == len(questions):
        return redirect(url_for('display_score'))

    # Ask the next question
    question = questions[len(history)]
    response = chat.send_message("rephrase the question in a softer tone, avoiding direct references to physical observations or limitations : " + question)
    rephrased_question = response.text
    history.append(("APP:", rephrased_question))
    return render_template('question.html', question=rephrased_question)

# Route for displaying the score
@app.route('/score')
def display_score():
    # Your score calculation logic here
    total_score = 0
    for i in range(len(history)):
        # Perform sentiment analysis on user's response
        user_input = history[i][1]
        document = language_v1.Document(content=user_input, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment

        # Determine sentiment score
        sentiment_score = 'positive' if sentiment.score >= 0 else 'negative'

        # Adjust scoring based on sentiment for questions 1-9
        if i < 9:
            total_score += 1 if sentiment_score == 'positive' else 0
        else:
            # For question 10, sentiment score is reversed
            total_score += 0 if sentiment_score == 'positive' else 1

    return render_template('score.html', total_score=total_score)

if __name__ == '__main__':
    app.run(debug=True)
