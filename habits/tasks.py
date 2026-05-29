from datetime import timedelta

from celery import shared_task
from habits.models import UsefulHabit
from django.utils import timezone

from habits.services import send_message_in_telegram

@shared_task
def useful_habit_reminder():
    now = timezone.now()
    notification_time = now + timedelta(minutes=5)

    habits_to_notify = UsefulHabit.objects.filter(
        next_notification__isnull=False,
        next_notification__lte=notification_time,
        next_notification__gte=now-timedelta(5)
    )

    for habit in habits_to_notify:
        try:
            message_text = f"""Напоминание о выполнении привычки.
Действие - {habit.action}
Место - {habit.place.name}
Время - {habit.time_for_habit}"""
            send_message_in_telegram(chat_id=habit.user.tg_chat_id,
                                     message_text=message_text)
            habit.update_after_notification()
        except Exception as e:
            print(f"Ошибка {e} во время отправки напоминания для привычки {habit.id}")
