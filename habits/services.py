import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_message_in_telegram(chat_id : str, message_text : str) -> None:
    bot_token = os.getenv("TELEGRAM_TOKEN")
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        "chat_id" : chat_id,
        "text" : message_text
    }
    response = requests.post(send_message_url, data=payload)