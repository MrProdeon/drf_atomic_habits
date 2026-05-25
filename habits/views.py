from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from habits.models import UsefulHabit, PleasantHabit, Place
from rest_framework.response import Response

from habits.serializer import UsefulHabitSerializer, PleasantHabitSerializer, PlaceSerializer


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

class CreateUsefulHabitAPIView(CreateAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreatePleasantHabitAPIView(CreateAPIView):
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UsefulHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer

class PleasantHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer

class PlaceCreateAPIView(CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
