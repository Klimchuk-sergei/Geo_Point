from django.contrib.auth.models import User
from django.contrib.gis.geos import Point as GeoPoint
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Point


class PointAPITests(APITestCase):
    def setUp(self):
        # Основной пользователь
        self.user = User.objects.create_user(username="stalker", password="password123")
        # Авторизация основного пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_point(self):
        url = reverse("point-list")

        data = {
            "name": "Схрон",
            "description": "Схрон с маслинами",
            "location": {"type": "Point", "coordinates": [39.104183, 44.989960]},
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Point.objects.count(), 1)

        new_point = Point.objects.first()
        self.assertEqual(new_point.name, "Схрон")
        self.assertEqual(new_point.description, "Схрон с маслинами")
        self.assertEqual(new_point.location.x, 39.104183)
        self.assertEqual(new_point.location.y, 44.989960)
        self.assertEqual(new_point.created_by, self.user)

    # точка А 39.123961, 44.994306 точка Б 39.117956,44.633295
    def test_search_radius(self):
        """Проверка поиска точек в радиусе, близкая точка А находится, а точка Б за пределами радиуса не находится"""
        url = reverse("point-search")

        Point.objects.create(
            name="Точка А", description="Цель поиска", created_by=self.user, location=GeoPoint(44.994306, 39.123961)
        )
        Point.objects.create(
            name="Точка Б",
            description="За пределами радиуса",
            created_by=self.user,
            location=GeoPoint(44.633295, 39.117956),
        )

        params = {"latitude": 39.123961, "longitude": 44.994306, "radius": 1000}  # радиус поиска 1 км

        response = self.client.get(url, params, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        if "results" in data:
            results_list = data["results"]
        else:
            results_list = data
        self.assertEqual(len(results_list), 1, f"Ожидаем 1 точку, получено: {len(results_list)}")
        self.assertEqual(results_list[0]["name"], "Точка А")

    def test_anonymous_access(self):
        """Проверка доступа анонимного пользователя к API"""
        self.client.force_authenticate(user=None)  # разлогиниваем пользователя
        url = reverse("point-list")
        response = self.client.get(url, format="json")  # получаем список точек
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )  # получаем ответ и видим что нас не пускает

    def test_delete_point(self):
        """Проверка удаления точки другим пользователем"""
        other_user = User.objects.create_user(username="kaban", password="password123")

        kaban_point = Point.objects.create(
            name="Точка kabana",
            description="схрон kabana",
            created_by=other_user,
            location=GeoPoint(44.994306, 39.123961),
        )

        url = reverse("point-detail", args=[kaban_point.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
