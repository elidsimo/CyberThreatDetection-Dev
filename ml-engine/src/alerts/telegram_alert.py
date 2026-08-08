"""
Envoi d'alertes via un bot Telegram (API Bot officielle, gratuite).
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_alert(message):
    """Envoie un message via le bot Telegram. Retourne True en cas de succès, False sinon."""
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"Échec envoi Telegram : statut {response.status_code} — {response.text}")
            return False
        return True
    except Exception as e:
        print(f"Échec envoi Telegram : {e}")
        return False