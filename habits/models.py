from django.db import models
from django.db.models import CASCADE, SET_NULL

from users.models import CustomUser


# Create your models here.
class Place(models.Model):
    """
    Модель места выполнения привычки
    """
    name = models.CharField(max_length=250, verbose_name="Место выполнения привычки", null=False, blank=False)

    class Meta:
        verbose_name = 'Место выполнения привычки'
        verbose_name_plural = 'Места выполнения привычек'

    def __str__(self):
        return self.name


class PleasantHabit(models.Model):
    """
    Модель приятной привычки
    """
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE, verbose_name="Создатель привычки",
                             related_name="pleasant_habits")
    place = models.ForeignKey(to=Place, on_delete=SET_NULL, verbose_name="Место выполнения привычки",
                              related_name="pleasant_habits_at_this_place")
    time_for_habit = models.DateTimeField(verbose_name="Время для выполнения привычки")
    action = models.CharField(max_length=250, verbose_name="Действие")
    periodicity = models.PositiveIntegerField(verbose_name="Переодичность выполнения для напоминания в днях")
    lead_time = models.IntegerField(verbose_name="Время выполнения в минутах")
    is_public = models.BooleanField(verbose_name="Признак публичности")

    def __str__(self):
        return self.name


class UsefulHabit(models.Model):
    """
    Модель полезной привычки
    """
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE, verbose_name="Создатель привычки", related_name="userful_habits")
    place = models.ForeignKey(to=Place, on_delete=SET_NULL, verbose_name="Место выполнения привычки",
                              related_name="userful_habits_at_this_place")
    time_for_habit = models.DateTimeField(verbose_name="Время для выполнения привычки")
    action = models.CharField(max_length=250, verbose_name="Действие")
    periodicity = models.PositiveIntegerField(verbose_name="Переодичность выполнения для напоминания в днях")
    text_reward = models.CharField(max_length=250, null=True, blank=True, verbose_name="Вознаграждение")
    pleasant_habit_reward = models.ForeignKey(to=PleasantHabit, verbose_name="Приятная привычка в награду", null=True,
                                              blank=True,
                                              related_name="related_userful_habits")
    lead_time = models.IntegerField(verbose_name="Время выполнения в минутах")
    is_public = models.BooleanField(verbose_name="Признак публичности")
