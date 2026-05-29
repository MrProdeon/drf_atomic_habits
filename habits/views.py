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
    """Получение списка полезных привычек для пользователя, делающего запрос"""
    pagination_class = MyPageNumberPagination
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UsefulHabit.objects.filter(user=self.request.user)


class UserPleasantsAPIView(ListAPIView):
    """Получение списка приятных привычек для пользователя, делающего запрос"""
    pagination_class = MyPageNumberPagination
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PleasantHabit.objects.filter(user=self.request.user)


class PublicUsefulHabits(ListAPIView):
    """Получение списка публичных полезных привычек"""
    serializer_class = UsefulHabitSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        return UsefulHabit.objects.filter(is_public=True)


class PublicPleasantHabits(ListAPIView):
    """Получение списка публичных приятных привычек"""
    serializer_class = PleasantHabitSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        return PleasantHabit.objects.filter(is_public=True)


class CreateUsefulHabitAPIView(CreateAPIView):
    """Создание полезной привычки"""
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreatePleasantHabitAPIView(CreateAPIView):
    """Создание приятной привычки"""
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UsefulHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование и удаление полезной привычки.
    Действие определяется в зависимости от метода запроса."""
    queryset = UsefulHabit.objects.all()
    serializer_class = UsefulHabitSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]


class PleasantHabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование и удаление приятной привычки.
    Действие определяется в зависимости от метода запроса."""
    queryset = PleasantHabit.objects.all()
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]


class PlaceCreateAPIView(CreateAPIView):
    """Создание места для выполнения привычки"""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PlaceListAPIView(ListAPIView):
    """Получение мест для выполнения привычки. Вернет места того пользователя, который их запрашивает."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Place.objects.filter(owner=self.request.user)

class PlaceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование и удаление места для выполнения привычки.
    Действие определяется в зависимости от метода запроса."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsUserOwner]
