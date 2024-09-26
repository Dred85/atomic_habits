
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.ru')
        self.habit1 = Habit.objects.create(
            place='home',
            time='14:00',
            action='VK',
            sign_of_a_pleasant_habit=True,
            frequency=1,
            time_to_complete='20',
            owner=self.user,
        )
        self.habit2 = Habit.objects.create(
            place='home',
            time='14:00',
            action='VK',
            sign_of_a_pleasant_habit=True,
            frequency=1,
            time_to_complete='20',
            sign_of_publicity=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """ Тестирование создания привычки """
        url = reverse('habits:habit-create')
        data = {
            'place': 'street',
            'time': '14:00',
            'action': 'jogging',
            'award': 'ice cream',
            'frequency': 1,
            'time_to_complete': 120
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Habit.objects.filter(owner=self.user).count())

    def test_update_habit(self):
        """ Тестирование редактирования привычки """
        url = reverse('habits:habit-update', args=[self.habit1.pk])
        data = {
            'place': 'street'
        }
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), 'street')

    def test_destroy_habit(self):
        """ Тестирование удаления привычки """
        url = reverse('habits:habit-delete', args=[self.habit1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Habit.objects.all().count())

    def test_list_habit(self, null=None):
        """ Тестирование вывода списка привычек """
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    'id': self.habit1.pk,
                    'time_to_complete': '00:00:20',
                    'frequency': self.habit1.frequency,
                    'place': self.habit1.place,
                    'time': '14:00:00',
                    'date': '2024-09-16',
                    'action': self.habit1.action,
                    'sign_of_a_pleasant_habit': self.habit1.sign_of_a_pleasant_habit,
                    'award': null,
                    'sign_of_publicity': False,
                    'owner': self.habit1.owner.pk,
                    'related_habit': null,
                }
            ]
        }
        data = response.json()
        self.assertEqual(data, result)

    def test_list_public_habit(self, null=None):
        """ Тестирование вывода списка публичных привычек """
        url = reverse('habits:habit-public')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    'id': self.habit2.pk,
                    'time_to_complete': '00:00:20',
                    'frequency': self.habit2.frequency,
                    'place': self.habit2.place,
                    'time': '14:00:00',
                    'date': '2024-09-16',
                    'action': self.habit2.action,
                    'sign_of_a_pleasant_habit': self.habit2.sign_of_a_pleasant_habit,
                    'award': null,
                    'sign_of_publicity': True,
                    'owner': null,
                    'related_habit': null,
                }
            ]
        }
        data = response.json()
        self.assertEqual(data, result)

