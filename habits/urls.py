from django.contrib import admin
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserHabitsAPIView, CreateUsefulHabitAPIView, CreatePleasantHabitAPIView, PlaceCreateAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path("my_habits/", UserHabitsAPIView.as_view(), name="user-habits"),
    path("create/useful_habit/", CreateUsefulHabitAPIView.as_view(), name="create-useful-habit"),
    path("create/pleasant_habit/", CreatePleasantHabitAPIView.as_view(), name="create-pleasant-habit"),
    path("create/place/", PlaceCreateAPIView.as_view(), name="create-place")

]
