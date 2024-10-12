from datetime import timedelta
from django.utils import timezone
from celery import shared_task
import logging

from habits.models import Habit
from habits.services import send_tg_message

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def reminder(self):
    now = timezone.now().today()
    habits = Habit.objects.filter(time__gte=now.time())

    for habit in habits:
        owner = habit.owner.tg_chat_id
        time_ = habit.time.strftime("%H:%M")
        date = habit.date + timedelta(days=habit.frequency)

        if date == now.date():
            if owner:
                text = f'Привычка "{habit.action}" запланирована сегодня на {time_}.'

                try:
                    response = send_tg_message(text, owner)
                    if response.status_code != 200:
                        raise Exception(f"Ошибка отправки: код {response.status_code}")

                except Exception as e:
                    logger.error(
                        f"Ошибка при отправке сообщения пользователю {owner}: {str(e)}"
                    )
                    try:
                        self.retry(countdown=60, exc=e)
                    except self.MaxRetriesExceededError:
                        logger.error(
                            f"Превышено количество попыток отправки сообщения для {owner}"
                        )
            else:
                logger.warning(
                    f"tg_chat_id не указан для пользователя {habit.owner}. Уведомление не отправлено."
                )
