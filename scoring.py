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

answers = [
    ['Always', 'Usually', 'Sometimes', 'Rarely', 'Never'],
    ['Very easy', 'Quite easy', 'Quite difficult', 'Very difficult', 'Impossible'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never'],
    ['Always', 'Usually', 'Sometimes', 'Rarely', 'Never'],
    ['Very typical', 'Quite typical', 'Slightly unusual', 'Very unusual', 'My child doesn’t speak'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never'],
    ['Many times a day', 'A few times a day', 'A few times a week', 'Less than once a week', 'Never']
]

# Scoring rules
scoring = {
    'Always': 0,
    'Usually': 0,
    'Sometimes': 0,
    'Rarely': 1,
    'Never': 1,
    'Very easy': 0,
    'Quite easy': 0,
    'Quite difficult': 1,
    'Very difficult': 1,
    'Impossible': 1,
    'Many times a day': 0,
    'A few times a day': 0,
    'A few times a week': 0,
    'Less than once a week': 1,
    'Very typical': 0,
    'Quite typical': 0,
    'Slightly unusual': 1,
    'Very unusual': 1,
    'My child doesn’t speak': 1
}

# Recording user responses and calculating score
total_score = 0
for i, question in enumerate(questions):
    print("Chatbot:", question)
    for j, option in enumerate(answers[i]):
        print(f"{j+1}. {option}")

    while True:
        user_input = input("User: ").strip().capitalize()

        # Check if user input is a digit
        if user_input.isdigit():
            choice_index = int(user_input)
            if choice_index > 0 and choice_index <= len(answers[i]):
                user_response = answers[i][choice_index - 1]
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        else:
            # Check if user input is a valid answer
            if user_input in answers[i]:
                user_response = user_input
                break
            else:
                print("Invalid answer. Please choose from the provided options.")

    # Calculating score based on user response
    if i == 9 :
        total_score += (scoring[user_response] ^ 1)
    else:
        total_score += scoring[user_response]
    

print("Total Q-CHAT-10 Score:", total_score)
if total_score >= 3:
    print("The health professional may consider referring your child for a multi-disciplinary assessment.")
