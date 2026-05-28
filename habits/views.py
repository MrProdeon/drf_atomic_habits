from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from habits.models import UsefulHabit, PleasantHabit, Place
from rest_framework.response import Response

from habits.permissions import IsUserOwner
from habits.serializer import UsefulHabitSerializer, PleasantHabitSerializer, PlaceSerializer
from habits.paginators import MyPageNumberPagination


# Create your views here.
class UserUsefulHabitsAPIView(ListAPIView):
    pagination_class = MyPageNumberPagination
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UsefulHabit.objects.filter(user=self.request.user)


class UserPleasantsAPIView(ListAPIView):
    pagination_class = MyPageNumberPagination
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PleasantHabit.objects.filter(user=self.request.user)


class PublicUsefulHabits(ListAPIView):
    serializer_class = UsefulHabitSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        return UsefulHabit.objects.filter(is_public=True)


class PublicPleasantHabits(ListAPIView):
    serializer_class = PleasantHabitSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        return PleasantHabit.objects.filter(is_public=True)


class CreateUsefulHabitAPIView(CreateAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreatePleasantHabitAPIView(CreateAPIView):
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UsefulHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]


class PleasantHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]


class PlaceCreateAPIView(CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PlaceListAPIView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Place.objects.filter(owner=self.request.user)

class PlaceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]
