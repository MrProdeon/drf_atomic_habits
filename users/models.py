from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.
class CustomUser(AbstractUser):
    tg_chat_id = models.CharField(max_length=10, verbose_name="id телеграм чата")

    objects = CustomUserManager()
    def __str__(self):
        return self.username