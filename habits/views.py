from django.shortcuts import render
from rest_framework.views import APIView
from habits.models import UsefulHabit, PleasantHabit
from rest_framework.response import Response

# Create your views here.
class UserHabitsAPIView(APIView):

    def get(self, request):
        user = self.request.user
        useful_habits = UsefulHabit.objects.filter(user=user)
        pleasant_habits = PleasantHabit.objects.filter(user=user)

        data = {
            "useful_habits" : UsefulHabitSerializer(useful_habits, many=True).data,
            "pleasant_habits": PleasantHabitSerializer(pleasant_habits, many=True).data
        }
        return Response(data)
