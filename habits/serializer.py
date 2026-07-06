from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Place, PleasantHabit, UsefulHabit
from users.serializers import CustomUserSerializer


class UsefulHabitSerializer(ModelSerializer):
    class Meta:
        model = UsefulHabit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):

        if self.instance is None:

            text_reward = data.get("text_reward")
            pleasant_reward = data.get("pleasant_habit_reward")

            errors = {}

            if text_reward and pleasant_reward:
                errors["non_field_errors"] = [
                    "Заполните только одно поле: text_reward ИЛИ pleasant_habit_reward"
                ]
            elif not text_reward and not pleasant_reward:
                errors["non_field_errors"] = [
                    "Необходимо заполнить либо text_reward, либо pleasant_habit_reward"
                ]

            if errors:
                raise serializers.ValidationError(errors)

            return data
        return data


class PleasantHabitSerializer(ModelSerializer):
    class Meta:
        model = PleasantHabit
        fields = "__all__"
        read_only_fields = ["user"]


class PlaceSerializer(ModelSerializer):
    class Meta:
        read_only_fields = ["owner"]
        model = Place
        fields = "__all__"
