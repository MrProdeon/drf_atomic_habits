from datetime import timedelta

from celery import shared_task
from habits.models import UsefulHabit, PleasantHabit
from django.utils import timezone

from habits.services import send_message_in_telegram, send_notifications



@shared_task
def useful_habit_reminder():
    now = timezone.now()
    notification_time = now + timedelta(minutes=5)

    habits_to_notify = UsefulHabit.objects.filter(
        next_notification__isnull=False,
        next_notification__lte=notification_time,
        next_notification__gte=now - timedelta(minutes=5)
    )

    send_notifications(habits_to_notify)

@shared_task
def pleasant_habit_reminder():
    now = timezone.now()
    notification_time = now + timedelta(minutes=5)

    habits_to_notify = PleasantHabit.objects.filter(
        next_notification__isnull=False,
        next_notification__lte=notification_time,
        next_notification__gte=now - timedelta(minutes=5)
    )

    send_notifications(habits_to_notify)
