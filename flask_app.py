#app config chatbot
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Google AI Studio API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY in the .env file.")
genai.configure(api_key=GOOGLE_API_KEY)

# Define the bot's role here
BOT_ROLE = "Tu eres un Project Manager y solo respondes preguntas relacionadas con lo que haces, tus respuestas son cortas, estás muy chistoso."  # You can change this to any role you want
PAGE_TITLE = "ChatBot: Project Manager" # Addded variable for the title
INPUT_PLACEHOLDER = "Pregúntame algo..." # Added variable for the input placeholder

model = genai.GenerativeModel('gemini-2.0-flash-lite')

def generate_response(prompt):
    chat = model.start_chat(history=[])
    # Include the role in the prompt
    role_prompt = f"As a {BOT_ROLE}, respond to the following: {prompt}"
    response = chat.send_message(role_prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (for testing in JupyterLab or as a standalone script)
    user_input = "Tell me about a reliable SUV."
    bot_response = generate_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot ({BOT_ROLE}): {bot_response}")

#app para ejecutar flask
from flask import Flask, render_template, request
from chatbot_logic import generate_response, BOT_ROLE, PAGE_TITLE, INPUT_PLACEHOLDER # Import the new variables
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Load Google AI Studio API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY in the .env file.")

app = Flask(__name__)

print(f"Python Executable: {sys.executable}")

@app.route("/")
def index():
    # Pass the variables to the template
    return render_template("index.html", page_title=PAGE_TITLE, input_placeholder=INPUT_PLACEHOLDER)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    bot_response = generate_response(user_input)
    return {"response": bot_response}

if __name__ == "__main__":
    app.run(debug=True)
