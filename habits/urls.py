from django.contrib import admin
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserUsefulHabitsAPIView, UserPleasantsAPIView, CreateUsefulHabitAPIView, \
    CreatePleasantHabitAPIView, PlaceCreateAPIView, \
    UsefulHabitRetrieveUpdateDestroyAPIView, PleasantHabitRetrieveUpdateDestroyAPIView, \
    PlaceRetrieveUpdateDestroyAPIView, PublicUsefulHabits, PublicPleasantHabits

app_name = HabitsConfig.name

urlpatterns = [
    # habits
    path("user_habits/useful/", UserUsefulHabitsAPIView.as_view(), name="user-useful-habits"),
    path("user_habits/pleasant/", UserPleasantsAPIView.as_view(), name="user-pleasant-habits"),
    path("public_habits/useful/", PublicUsefulHabits.as_view(), name="public-useful-habits"),
    path("public_habits/pleasant/", PublicPleasantHabits.as_view(), name="public-pleasant-habits"),
    path("useful_habit/create/", CreateUsefulHabitAPIView.as_view(), name="create-useful-habit"),
    path("pleasant_habit/create/", CreatePleasantHabitAPIView.as_view(), name="create-pleasant-habit"),
    path("useful_habit/<int:pk>/", UsefulHabitRetrieveUpdateDestroyAPIView.as_view(), name="useful-habit"),
    path("pleasant_habit/<int:pk>/", PleasantHabitRetrieveUpdateDestroyAPIView.as_view(), name="pleasant-habit"),

    # place
    path("place/create/", PlaceCreateAPIView.as_view(), name="create-place"),
    path("place/<int:pk>/", PlaceRetrieveUpdateDestroyAPIView.as_view(), name="place")

]
