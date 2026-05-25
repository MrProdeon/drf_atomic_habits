from django.contrib import admin
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserHabitsAPIView, CreateUsefulHabitAPIView, CreatePleasantHabitAPIView, PlaceCreateAPIView, \
    UsefulHabitRetrieveUpdateDestroyAPIView, PleasantHabitRetrieveUpdateDestroyAPIView, PublicHabitsAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path("my_habits/", UserHabitsAPIView.as_view(), name="user-habits"),
    path("public_habits/", PublicHabitsAPIView.as_view(), name="public-habits"),
    path("create/useful_habit/", CreateUsefulHabitAPIView.as_view(), name="create-useful-habit"),
    path("create/pleasant_habit/", CreatePleasantHabitAPIView.as_view(), name="create-pleasant-habit"),
    path("create/place/", PlaceCreateAPIView.as_view(), name="create-place"),
    path("useful_habit/<int:pk>/", UsefulHabitRetrieveUpdateDestroyAPIView.as_view(), name="useful-habit"),
    path("pleasant_habit/<int:pk>/", PleasantHabitRetrieveUpdateDestroyAPIView.as_view(), name="pleasant-habit")

]
