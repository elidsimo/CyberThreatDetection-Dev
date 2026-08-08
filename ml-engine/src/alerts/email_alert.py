"""
Envoi d'alertes par email via SMTP (Gmail).
Utilise smtplib, module standard Python — pas de dépendance supplémentaire.
"""

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")


def send_email_alert(subject, body):
    """Envoie un email d'alerte. Retourne True en cas de succès, False sinon."""
    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = SMTP_USER
    message["To"] = ALERT_EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_USER, [ALERT_EMAIL_TO], message.as_string())
        return True
    except Exception as e:
        print(f"Échec envoi email : {e}")
        return False