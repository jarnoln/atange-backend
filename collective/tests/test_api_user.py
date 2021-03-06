import json
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase


class UserInfoViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("user_info", args=["superman"]), "/api/user/superman/")

    def test_get_user_info(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = client.get(reverse("user_info", args=["superman"]))
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out["email"], "clark@dailyplanet.com")
        self.assertEqual(data_out["first_name"], "Clark")
        self.assertEqual(data_out["last_name"], "Kent")

    def test_no_such_user(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = client.get(reverse("user_info", args=["nobody"]))
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_info(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data_in = {
            "email": "kalel@krypton.planet",
            "first_name": "Kal",
            "last_name": "El",
        }
        response = client.put(reverse("user_info", args=[user.username]), data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out["email"], "kalel@krypton.planet")
        self.assertEqual(data_out["first_name"], "Kal")
        self.assertEqual(data_out["last_name"], "El")
