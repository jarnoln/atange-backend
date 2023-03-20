import json
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import UserDescription


class UserExtraInfoViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("user_description", args=["superman"]), "/api/user/superman/description/")

    def test_get_user_description(self):
        client = APIClient()
        user = self.create_user()
        response = client.get(reverse("user_description", args=[user.username]))
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out["description"], "")
        self.assertEqual(data_out["candidate_number"], None)
        self.assertEqual(data_out["home_page"], None)

    def test_no_such_user(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = client.get(reverse("user_description", args=["nobody"]))
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_extra_info(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data_in = {
            "description": "Defender of Justice",
            "candidate_number": 2,
            "home_page": "https://superman.com"
        }
        response = client.put(reverse("user_description", args=[user.username]), data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        description = UserDescription.objects.get(user=user)
        self.assertEqual(description.description, "Defender of Justice")
        self.assertEqual(description.home_page, "https://superman.com")
        self.assertEqual(description.candidate_number, 2)
        self.assertEqual(data_out["description"], "Defender of Justice")
