from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from habits.models import Place, UsefulHabit, PleasantHabit
from datetime import time, timedelta
from django.utils import timezone


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
            "text_reward": "test reward"
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
        self.assertEqual(parse_useful_response["place"], self.place.id)
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

        self.useful_url = reverse("habits:useful-habit", kwargs={"pk": self.useful_habit.id})
        self.pleasant_url = reverse("habits:pleasant-habit", kwargs={"pk": self.pleasant_habit.id})

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
        useful_response = self.client.patch(self.useful_url, data={"action": "test_patch_action"})
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


class UserHabitsListTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.place = Place.objects.create(name="test_place", owner=self.user)

        self.useful_habit_1 = UsefulHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(12, 0, 0),
            action="useful action 1",
            periodicity=1,
            lead_time=100,
            is_public=True,
            text_reward="reward 1"
        )
        self.useful_habit_2 = UsefulHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(14, 0, 0),
            action="useful action 2",
            periodicity=2,
            lead_time=60,
            is_public=False,
            text_reward="reward 2"
        )

        self.pleasant_habit_1 = PleasantHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(21, 0, 0),
            action="pleasant action 1",
            periodicity=1,
            lead_time=120,
            is_public=True
        )
        self.pleasant_habit_2 = PleasantHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(22, 0, 0),
            action="pleasant action 2",
            periodicity=3,
            lead_time=90,
            is_public=False
        )

        self.other_user = CustomUser.objects.create_user(username="otheruser", password="otherpassword")
        self.other_place = Place.objects.create(name="other_place", owner=self.other_user)
        UsefulHabit.objects.create(
            user=self.other_user,
            place=self.other_place,
            time_for_habit=time(10, 0, 0),
            action="other useful",
            periodicity=1,
            lead_time=50,
            is_public=True,
            text_reward="other reward"
        )

        self.useful_url = reverse("habits:user-useful-habits")
        self.pleasant_url = reverse("habits:user-pleasant-habits")

    def test_user_useful_habits_list(self):
        response = self.client.get(self.useful_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        if 'results' in response_data:
            results = response_data['results']
        else:
            results = response_data

        self.assertEqual(len(results), 2)
        actions = [habit["action"] for habit in results]
        self.assertIn("useful action 1", actions)
        self.assertIn("useful action 2", actions)

    def test_user_pleasant_habits_list(self):
        response = self.client.get(self.pleasant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        if 'results' in response_data:
            results = response_data['results']
        else:
            results = response_data

        self.assertEqual(len(results), 2)
        actions = [habit["action"] for habit in results]
        self.assertIn("pleasant action 1", actions)
        self.assertIn("pleasant action 2", actions)


class PublicHabitsListTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.user2 = CustomUser.objects.create_user(username="testuser2", password="testpassword2")
        self.client.force_authenticate(user=self.user)

        self.place = Place.objects.create(name="test_place", owner=self.user)
        self.place2 = Place.objects.create(name="test_place2", owner=self.user2)

        self.public_useful_1 = UsefulHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(12, 0, 0),
            action="public useful 1",
            periodicity=1,
            lead_time=100,
            is_public=True,
            text_reward="reward 1"
        )
        self.public_useful_2 = UsefulHabit.objects.create(
            user=self.user2,
            place=self.place2,
            time_for_habit=time(14, 0, 0),
            action="public useful 2",
            periodicity=2,
            lead_time=60,
            is_public=True,
            text_reward="reward 2"
        )

        UsefulHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(16, 0, 0),
            action="private useful",
            periodicity=1,
            lead_time=80,
            is_public=False,
            text_reward="private reward"
        )

        self.public_pleasant_1 = PleasantHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(21, 0, 0),
            action="public pleasant 1",
            periodicity=1,
            lead_time=120,
            is_public=True
        )
        self.public_pleasant_2 = PleasantHabit.objects.create(
            user=self.user2,
            place=self.place2,
            time_for_habit=time(22, 0, 0),
            action="public pleasant 2",
            periodicity=3,
            lead_time=90,
            is_public=True
        )

        PleasantHabit.objects.create(
            user=self.user,
            place=self.place,
            time_for_habit=time(23, 0, 0),
            action="private pleasant",
            periodicity=1,
            lead_time=30,
            is_public=False
        )

        self.public_useful_url = reverse("habits:public-useful-habits")
        self.public_pleasant_url = reverse("habits:public-pleasant-habits")

    def test_public_useful_habits_list(self):
        response = self.client.get(self.public_useful_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        if 'results' in response_data:
            results = response_data['results']
        else:
            results = response_data

        self.assertEqual(len(results), 2)
        actions = [habit["action"] for habit in results]
        self.assertIn("public useful 1", actions)
        self.assertIn("public useful 2", actions)

    def test_public_pleasant_habits_list(self):
        response = self.client.get(self.public_pleasant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        if 'results' in response_data:
            results = response_data['results']
        else:
            results = response_data

        self.assertEqual(len(results), 2)
        actions = [habit["action"] for habit in results]
        self.assertIn("public pleasant 1", actions)
        self.assertIn("public pleasant 2", actions)


class PlaceAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.other_user = CustomUser.objects.create_user(username="otheruser", password="otherpassword")

        self.place = Place.objects.create(
            name="test_place",
            owner=self.user
        )

        self.other_place = Place.objects.create(
            name="other_place",
            owner=self.other_user
        )

        self.create_url = reverse("habits:create-place")
        self.place_detail_url = reverse("habits:place", kwargs={"pk": self.place.id})
        self.other_place_detail_url = reverse("habits:place", kwargs={"pk": self.other_place.id})

    def test_create_place(self):
        place_data = {"name": "new place"}

        response = self.client.post(self.create_url, place_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(response_data["name"], "new place")
        self.assertEqual(response_data["owner"], self.user.id)

    def test_create_place_empty_name(self):
        place_data = {"name": ""}

        response = self.client.post(self.create_url, place_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_place(self):
        response = self.client.get(self.place_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["name"], "test_place")
        self.assertEqual(response_data["owner"], self.user.id)

    def test_get_other_user_place(self):
        response = self.client.get(self.other_place_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_place(self):
        update_data = {"name": "updated place name"}

        response = self.client.patch(self.place_detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["name"], "updated place name")
        self.assertEqual(response_data["owner"], self.user.id)

    def test_update_other_user_place(self):
        response = self.client.patch(self.other_place_detail_url, {"name": "hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_place(self):
        response = self.client.delete(self.place_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(self.place_detail_url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_place(self):
        response = self.client.delete(self.other_place_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(Place.objects.filter(id=self.other_place.id).exists())


class UnauthorizedAccessTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
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

    def test_unauthenticated_access_to_detail_endpoints(self):
        self.client.force_authenticate(user=None)

        urls_to_test = [
            reverse("habits:useful-habit", kwargs={"pk": self.useful_habit.id}),
            reverse("habits:place", kwargs={"pk": self.place.id}),
        ]

        for url in urls_to_test:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_create_habit(self):
        self.client.force_authenticate(user=None)

        create_urls = [
            reverse("habits:create-useful-habit"),
            reverse("habits:create-pleasant-habit"),
            reverse("habits:create-place"),
        ]

        for url in create_urls:
            response = self.client.post(url, {})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update_delete(self):
        self.client.force_authenticate(user=None)

        update_urls = [
            reverse("habits:useful-habit", kwargs={"pk": self.useful_habit.id}),
            reverse("habits:place", kwargs={"pk": self.place.id}),
        ]

        for url in update_urls:
            patch_response = self.client.patch(url, {})
            self.assertEqual(patch_response.status_code, status.HTTP_401_UNAUTHORIZED)

            delete_response = self.client.delete(url)
            self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)