from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from habits.models import Place, UsefulHabit, PleasantHabit
from datetime import time


# Create your tests here.
class CreateHabitsTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.place = Place.objects.create(name="test_place", owner=self.user)

        self.useful_url = reverse("habits:create-useful-habit")
        self.useful_data = {
            "time_for_habit": "12:00",
            "action": "test action",
            "periodicity": 1,
            "lead_time": 100,
            "is_public": True,
            "place": self.place.id,
            "text_reward": "test rewatd"
        }

        self.pleasant_url = reverse("habits:create-pleasant-habit")
        self.pleasant_data = {
            "time_for_habit": "21:00",
            "action": "pleasant action",
            "periodicity": 1,
            "lead_time": 100,
            "is_public": False,
            "place": self.place.id,
        }

    def test_post(self):
        useful_response = self.client.post(self.useful_url, self.useful_data)
        parse_useful_response = useful_response.json()
        self.assertEqual(useful_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(parse_useful_response["action"], "test action")
        self.assertEqual(parse_useful_response["place"], 1)
        self.assertEqual(parse_useful_response["is_public"], True)

        pleasant_response = self.client.post(self.pleasant_url, self.pleasant_data)
        parse_pleasant_response = pleasant_response.json()
        self.assertEqual(pleasant_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(parse_pleasant_response["action"], "pleasant action")
        self.assertEqual(parse_pleasant_response["time_for_habit"], "21:00:00")
        self.assertEqual(parse_pleasant_response["is_public"], False)


class ActionsOnHabits(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.place = Place.objects.create(name="test_place", owner=self.user)

        self.useful_habit = UsefulHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(12, 0, 0),
            action="test action",
            periodicity=1,
            lead_time=100,
            is_public=True,
            text_reward="test reward"
        )
        self.pleasant_habit = PleasantHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(21, 0, 0),
            action="pleasant action",
            periodicity=1,
            lead_time=100,
            is_public=False
        )

        self.useful_url = reverse("habits:useful-habit", kwargs={"pk" : self.useful_habit.id})
        self.pleasant_url = reverse("habits:pleasant-habit", kwargs={"pk" : self.pleasant_habit.id})

    def test_get(self):
        useful_response = self.client.get(self.useful_url)
        parse_useful_response = useful_response.json()
        self.assertEqual(useful_response.status_code, status.HTTP_200_OK)
        self.assertEqual(parse_useful_response["action"], "test action")

        pleasant_response = self.client.get(self.pleasant_url)
        parse_pleasant_response = pleasant_response.json()
        self.assertEqual(pleasant_response.status_code, status.HTTP_200_OK)
        self.assertEqual(parse_pleasant_response["action"], "pleasant action")

    def test_put(self):
        useful_response = self.client.patch(self.useful_url, data={"action" : "test_patch_action"})
        self.assertEqual(useful_response.status_code, status.HTTP_200_OK)
        self.assertEqual(useful_response.json()["action"], "test_patch_action")

        pleasant_response = self.client.patch(self.pleasant_url, data={"action": "pleasant_patch"})
        self.assertEqual(pleasant_response.status_code, status.HTTP_200_OK)
        self.assertEqual(pleasant_response.json()["action"], "pleasant_patch")

    def test_delete(self):
        useful_response = self.client.delete(self.useful_url)
        self.assertEqual(useful_response.status_code, status.HTTP_204_NO_CONTENT)

        pleasant_response = self.client.delete(self.pleasant_url)
        self.assertEqual(pleasant_response.status_code, status.HTTP_204_NO_CONTENT)