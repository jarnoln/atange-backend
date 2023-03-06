import json
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import UserGroup


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


class UserMembershipsViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("user_memberships", args=["superman"]), "/api/user/superman/memberships/")

    def test_get_user_memberships(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("user_memberships", args=[user.username])
        response = client.get(url)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data_out), 0)

        ug_1 = UserGroup.objects.create(name='metropolis', title='Metropolis', type='district')
        ug_2 = UserGroup.objects.create(name='kryptonian', title='Kryptonian', type='species')
        ug_1.add_member(user)
        ug_2.add_member(user)

        response = client.get(url)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "metropolis")
        self.assertEqual(data_out[0]["title"], "Metropolis")
        self.assertEqual(data_out[0]["type"], "district")
        self.assertEqual(data_out[1]["name"], "kryptonian")
        self.assertEqual(data_out[1]["title"], "Kryptonian")
        self.assertEqual(data_out[1]["type"], "species")
