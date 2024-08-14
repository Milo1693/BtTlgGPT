from flask import Flask
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Créer une application Flask
app = Flask(__name__)

# Clé API Google Generative Language
API_KEY = "AIzaSyD1sIW43FYKHF16pev53JARHg3TTUFF-tI"  # Remplace par ta clé API

# Fonction pour interroger l'API Google Generative Language
def ask_google_generative(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    try:
        response_json = response.json()
        # Vérification des clés
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                return candidate["content"]["parts"][0]["text"]
            else:
                return "Erreur : Les données attendues ne sont pas disponibles dans la réponse."
        else:
            return "Erreur : La réponse de l'API ne contient pas de candidats."
    except ValueError:
        return "Erreur : Impossible de décoder la réponse JSON."

# Fonction pour gérer les messages du bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = ask_google_generative(user_message)
    await update.message.reply_text(response)

# Fonction pour démarrer le bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenue sur le bot ! Pose-moi une question.")

# Définir un itinéraire pour la page d'accueil
@app.route('/')
def hello_world():
    return "Ce bot est fabriqué par Manifatic et actuellement il est hébergé et en direct pour tout Manifatic"

if __name__ == "__main__":
    # Crée et configure le bot avec ton token Telegram
    bot_token = "7388184733:AAFveKo2QPJb0QZNMPSjpp7rcnuYdp6DUS0"  # Remplace par ton token
    application = ApplicationBuilder().token(bot_token).build()

    # Ajoute les gestionnaires de commandes et de messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Lancer le bot Telegram dans un thread séparé
    import threading
    threading.Thread(target=application.run_polling).start()

    # Exécuter l'application Flask
    app.run(host="0.0.0.0", port=5000)
