import os

import requests
from dotenv import load_dotenv

load_dotenv()


def send_message_in_telegram(chat_id: str, message_text: str) -> None:
    bot_token = os.getenv("TELEGRAM_TOKEN")
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message_text}
    response = requests.post(send_message_url, data=payload)
    return response


def send_notifications(habits_to_notify):
    for habit in habits_to_notify:
        if habit.user.tg_chat_id:
            try:
                message_text = (f"Напоминание о привычке\nДействие - {habit.action}\n"
                                f"Место - {habit.place.name}\nВремя - {habit.time_for_habit}")
                send_message_in_telegram(
                    chat_id=habit.user.tg_chat_id, message_text=message_text
                )
                habit.update_after_notification()
            except Exception as e:
                print(
                    f"Ошибка {e} во время отправки напоминания для привычки {habit.id}"
                )
        else:
            continue
