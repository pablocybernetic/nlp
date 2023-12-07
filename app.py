from flask import Flask, request, jsonify
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import random

app = Flask(__name__)

# Initialize NLTK components
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Sample conversation data
conversation_data = {
    "greeting": ["hi", "hello", "hey", "howdy"],
    "farewell": ["bye", "goodbye", "see you"],
    "thanks": ["thank", "thanks", "thank you"],
    "responses": {
        "greeting": ["Hello!", "Hi there!", "Hey!"],
        "farewell": ["Goodbye!", "Bye!", "See you later!"],
        "thanks": ["You're welcome!", "No problem!", "Anytime!"]
    }
}

# Preprocess text: tokenize, lemmatize
def preprocess(text):
    tokens = word_tokenize(text.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

# Simple text matching to generate responses
def generate_response(tokens):
    for intent, keywords in conversation_data.items():
        if intent != "responses":
            for keyword in keywords:
                if keyword in tokens:
                    return random.choice(conversation_data["responses"][intent])
    return "I'm sorry, I didn't understand that."

# Endpoint for handling incoming messages
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    processed_message = preprocess(message)
    response = generate_response(processed_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
