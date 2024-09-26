from datetime import timedelta

from rest_framework import serializers


class SimultaneousSelectionValidator:
    """Валидатор одновременного выбора поля вознаграждения и
    поля связанной привычки."""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        if self.field1 in value and self.field2 in value:
            raise serializers.ValidationError(
                "Не должно быть заполнено одновременно "
                "и поле вознаграждения, и поле связанной "
                "привычки. Можно заполнить только одно из "
                "двух полей."
            )


class TimeValidator:
    """Валидатор на время выполнения привычки"""

    def __call__(self, value):
        if value > timedelta(seconds=120):
            raise serializers.ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )


class RelatedHabitValidator:
    """Валидатор на связанные привычки """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if not tmp_val.sign_of_a_pleasant_habit:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                )


class PleasantHabitValidator:
    """Валидатор на приятную привычку"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            value_ = dict(value)
            if value_.get("award") or value_.get("related_habit"):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class FrequencyHabitValidator:
    """Валидатор на периодичность выполнения привычки"""

    def __call__(self, value):
        if 0 < value > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )
