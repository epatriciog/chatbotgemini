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
