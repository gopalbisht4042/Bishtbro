import os
import time
import requests

# Official appointment page URL
URL = os.environ.get("APPOINTMENT_URL", "")

# Telegram settings
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Words that may indicate availability
AVAILABLE_WORDS = [
    "appointment available",
    "available slots",
    "select appointment",
    "book appointment",
]

def telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram settings are missing.")
        return

    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        api,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=20,
    )

def check_page():
    if not URL:
        raise RuntimeError("APPOINTMENT_URL is not configured.")

    response = requests.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )

    response.raise_for_status()
    page = response.text.lower()

    for word in AVAILABLE_WORDS:
        if word.lower() in page:
            return True, word

    return False, None


if __name__ == "__main__":
    try:
        available, matched = check_page()

        if available:
            message = (
                "🇩🇪 Germany appointment availability detected!\n\n"
                f"Matched: {matched}\n"
                f"Check the official page:\n{URL}"
            )

            telegram_alert(message)
            print(message)
        else:
            print("No matching appointment availability detected.")

    except Exception as e:
        print(f"Monitor error: {e}")