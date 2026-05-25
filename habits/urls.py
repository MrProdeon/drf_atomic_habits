from django.contrib import admin
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserHabitsAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path("my_habits/", UserHabitsAPIView.as_view(), name="user-habits"),

]