from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    SimultaneousSelectionValidator,
    TimeValidator,
    RelatedHabitValidator,
    PleasantHabitValidator,
    FrequencyHabitValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    time_to_complete = serializers.DurationField(validators=[TimeValidator()])
    frequency = serializers.IntegerField(validators=[FrequencyHabitValidator()])

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            SimultaneousSelectionValidator(field1="award", field2="related_habit"),
            RelatedHabitValidator(field="related_habit"),
            PleasantHabitValidator(field="sign_of_a_pleasant_habit"),
        ]
