# app.py (Versión final consolidada para Render)

from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuración y Lógica de la IA (se ejecuta al importar el módulo) ---

# Carga variables de entorno (solo para desarrollo local).
# En Render, configurarás GOOGLE_API_KEY directamente en la interfaz.
load_dotenv()

# Carga la clave de la API de Google AI Studio
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Por favor, configura la GOOGLE_API_KEY. Para Render, hazlo en las 'Environment Variables' de tu servicio.")

genai.configure(api_key=GOOGLE_API_KEY)

# Define el rol del bot y otras constantes
BOT_ROLE = "Tu eres un Project Manager y solo respondes preguntas relacionadas con lo que haces, tus respuestas son cortas, estás muy chistoso."
PAGE_TITLE = "ChatBot: Project Manager"
INPUT_PLACEHOLDER = "Pregúntame algo..."

model = genai.GenerativeModel('gemini-2.0-flash-lite')

def generate_response(prompt):
    chat = model.start_chat(history=[])
    role_prompt = f"As a {BOT_ROLE}, responde a lo siguiente: {prompt}"
    response = chat.send_message(role_prompt)
    return response.text

# --- Aplicación Flask ---

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", page_title=PAGE_TITLE, input_placeholder=INPUT_PLACEHOLDER)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    bot_response = generate_response(user_input)
    return {"response": bot_response}

# NOTA: El bloque if __name__ == "__main__": con app.run() ha sido eliminado
# o comentado para el despliegue en producción como Render.
