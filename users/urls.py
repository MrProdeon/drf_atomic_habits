from users.apps import UsersConfig
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIVew

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIVew.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh_token/", TokenRefreshView.as_view(), name="refresh-token")

]
