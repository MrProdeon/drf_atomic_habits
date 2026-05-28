from django.contrib import admin
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserUsefulHabitsAPIView, UserPleasantsAPIView, CreateUsefulHabitAPIView, CreatePleasantHabitAPIView, PlaceCreateAPIView, \
    UsefulHabitRetrieveUpdateDestroyAPIView, PleasantHabitRetrieveUpdateDestroyAPIView, PublicHabitsAPIView, \
    PlaceRetrieveUpdateDestroyAPIView, PublicUsefulHabits, PublicPleasantHabits

app_name = HabitsConfig.name

urlpatterns = [
    # habits
    path("user_useful_habits/", UserUsefulHabitsAPIView.as_view(), name="user-useful-habits"),
    path("user_pleasant_habits/", UserPleasantsAPIView.as_view(), name="user-pleasant-habits"),
    path("public_useful_habits/", PublicUsefulHabits.as_view(), name="public-useful-habits"),
    path("public_pleasant_habits/", PublicPleasantHabits.as_view(), name="public-pleasant-habits"),
    path("create/useful_habit/", CreateUsefulHabitAPIView.as_view(), name="create-useful-habit"),
    path("create/pleasant_habit/", CreatePleasantHabitAPIView.as_view(), name="create-pleasant-habit"),
    path("useful_habit/<int:pk>/", UsefulHabitRetrieveUpdateDestroyAPIView.as_view(), name="useful-habit"),
    path("pleasant_habit/<int:pk>/", PleasantHabitRetrieveUpdateDestroyAPIView.as_view(), name="pleasant-habit"),

    # place
    path("create/place/", PlaceCreateAPIView.as_view(), name="create-place"),
    path("place/<int:pk>/", PlaceRetrieveUpdateDestroyAPIView.as_view(), name="place")

]
