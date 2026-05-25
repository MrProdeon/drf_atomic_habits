from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.core.exceptions import ValidationError

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
    place = models.ForeignKey(to=Place, on_delete=CASCADE, verbose_name="Место выполнения привычки",
                              related_name="pleasant_habits_at_this_place")
    time_for_habit = models.DateTimeField(verbose_name="Время для выполнения привычки")
    action = models.CharField(max_length=250, verbose_name="Действие")
    periodicity = models.PositiveIntegerField(verbose_name="Переодичность выполнения для напоминания в днях",
                                              validators=[
                                                  MinValueValidator(1,
                                                                    "Привычку нельзя выполнять чаще, чем раз в день"),
                                                  MaxValueValidator(7,
                                                                    message="Привычку можно выполнять не реже, чем раз в 7 дней")
                                              ])
    lead_time = models.IntegerField(verbose_name="Время выполнения в секундах",
                                    validators=[
                                        MinValueValidator(1, "Время выполнения не может быть меньше секунды"),
                                        MaxValueValidator(120, "Время выполнения не может быть больше 120 секунды")
                                    ])
    is_public = models.BooleanField(verbose_name="Признак публичности")

    def __str__(self):
        return self.name


class UsefulHabit(models.Model):
    """
    Модель полезной привычки
    """
    user = models.ForeignKey(to=CustomUser, on_delete=CASCADE, verbose_name="Создатель привычки",
                             related_name="userful_habits")
    place = models.ForeignKey(to=Place, on_delete=CASCADE, verbose_name="Место выполнения привычки",
                              related_name="userful_habits_at_this_place")
    time_for_habit = models.DateTimeField(verbose_name="Время для выполнения привычки")
    action = models.CharField(max_length=250, verbose_name="Действие")
    periodicity = models.PositiveIntegerField(verbose_name="Переодичность выполнения для напоминания в днях",
                                              validators=[
                                                  MinValueValidator(1,
                                                                    "Привычку нельзя выполнять чаще, чем раз в день"),
                                                  MaxValueValidator(7,
                                                                    message="Привычку можно выполнять не реже, чем раз в 7 дней")
                                              ])
    text_reward = models.CharField(max_length=250, null=True, blank=True, verbose_name="Вознаграждение")
    pleasant_habit_reward = models.ForeignKey(to=PleasantHabit, on_delete=SET_NULL, verbose_name="Приятная привычка в награду", null=True,
                                              blank=True,
                                              related_name="related_userful_habits")
    lead_time = models.IntegerField(verbose_name="Время выполнения в секундах",
                                    validators=[
                                        MinValueValidator(1, "Время выполнения не может быть меньше секунды"),
                                        MaxValueValidator(120, "Время выполнения не может быть больше 120 секунды")
                                    ])
    is_public = models.BooleanField(verbose_name="Признак публичности")

    def clean(self):
        if self.text_reward and self.pleasant_habit_reward:
            raise ValidationError(
                "Для заполнения допускается ЛИБО text_reward, ЛИБО pleasant_habit_reward. Одновременное заполнение запрещено.")
        if not self.text_reward and not self.pleasant_habit_reward:
            raise ValidationError(
                "Необходимо заполнить либо поле text_reward, либо pleasant_habit_reward.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
