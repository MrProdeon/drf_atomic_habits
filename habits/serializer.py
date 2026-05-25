from rest_framework.serializers import ModelSerializer
from habits.models import UsefulHabit, PleasantHabit

class UsefulHabitSerializer(ModelSerializer):
    class Meta:
        model = UsefulHabit
        fields = "__all__"

class PleasantHabitSerializer(ModelSerializer):
    class Meta:
        models = PleasantHabit
        fields = "__all__"