from datetime import timedelta

from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              **NULLABLE,
                              verbose_name='создатель привычки')
    place = models.CharField(max_length=150,
                             verbose_name='место привычки')
    time = models.TimeField(verbose_name='время привычки')
    date = models.DateField(default='2024-09-26', verbose_name='дата привычки')
    action = models.CharField(max_length=150,
                              verbose_name='действие привычки')
    sign_of_a_pleasant_habit = models.BooleanField(default=False,
                                                   verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self',
                                      on_delete=models.SET_NULL,
                                      **NULLABLE,
                                      verbose_name='связанная привычка')
    frequency = models.PositiveSmallIntegerField(default=1,
                                                 verbose_name='периодичность привычки, в днях')
    award = models.CharField(max_length=255,
                             verbose_name='вознаграждение',
                             **NULLABLE)
    time_to_complete = models.DurationField(default=timedelta(seconds=20),
                                            verbose_name='время на выполнение')
    sign_of_publicity = models.BooleanField(default=False,
                                            verbose_name='признак публичности')

    def __str__(self):
        return f'{self.action}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
