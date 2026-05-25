from users.apps import UsersConfig
from django.contrib import admin
from django.urls import path

from users.views import UserCreateAPIVew

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIVew.as_view(), name="register"),

]
