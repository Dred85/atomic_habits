from datetime import timedelta
from django.utils import timezone
from celery import shared_task

from habits.models import Habit
from habits.services import send_tg_message


@shared_task
def reminder():
    now = timezone.now().today()
    habits = Habit.objects.filter(time__gte=now.time())
    for habit in habits:
        owner = habit.owner.tg_chat_id
        time_ = habit.time.strftime("%H:%M")
        date = habit.date + timedelta(days=habit.frequency)
        if date == now.date():
            if owner:
                text = f'Привычка "{habit.action}" запланирована сегодня на {time_}.'
                send_tg_message(text, owner)
