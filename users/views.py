from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from users.models import CustomUser
from users.serializers import CustomUserSerializer


# Create your views here.
class UserCreateAPIVew(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

