import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class UserGroupListViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(
            reverse("collective_user_groups", args=["jla"]),
            "/api/collective/jla/user_groups/",
        )
        self.assertEqual(
            reverse("collective_user_groups_by_type", args=["jla", "district"]),
            "/api/collective/jla/user_groups/type/district/",
        )
        self.assertEqual(reverse("user_groups"), "/api/user_groups/")
        self.assertEqual(
            reverse("user_groups_by_type", args=["district"]),
            "/api/user_groups/type/district/",
        )

    def test_get_collective_user_group_list(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        collective = Collective.objects.create(name="jla", title="JLA", creator=user)
        ug_1 = UserGroup.objects.create(
            name="gotham",
            title="Gotham",
            type="district",
            collective_name=collective.name,
        )
        ug_2 = UserGroup.objects.create(
            name="metropolis",
            title="Metropolis",
            type="district",
            collective_name=collective.name,
        )

        ug_3 = UserGroup.objects.create(
            name="human", title="Human", type="species", collective_name=collective.name
        )

        url = reverse("collective_user_groups", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 3)
        self.assertEqual(data_out[0]["name"], "gotham")
        self.assertEqual(data_out[0]["title"], "Gotham")
        self.assertEqual(data_out[0]["type"], "district")
        self.assertEqual(data_out[1]["name"], "metropolis")
        self.assertEqual(data_out[1]["title"], "Metropolis")
        self.assertEqual(data_out[1]["type"], "district")
        self.assertEqual(data_out[2]["name"], "human")
        self.assertEqual(data_out[2]["title"], "Human")
        self.assertEqual(data_out[2]["type"], "species")

        url = reverse(
            "collective_user_groups_by_type", args=[collective.name, "district"]
        )
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "gotham")
        self.assertEqual(data_out[0]["title"], "Gotham")
        self.assertEqual(data_out[0]["type"], "district")
        self.assertEqual(data_out[1]["name"], "metropolis")
        self.assertEqual(data_out[1]["title"], "Metropolis")
        self.assertEqual(data_out[1]["type"], "district")

        url = reverse(
            "collective_user_groups_by_type", args=[collective.name, "species"]
        )
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 1)
        self.assertEqual(data_out[0]["name"], "human")
        self.assertEqual(data_out[0]["title"], "Human")
        self.assertEqual(data_out[0]["type"], "species")

    def test_get_user_group_list(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        ug_1 = UserGroup.objects.create(name="gotham", title="Gotham", type="district", collective_name=None)
        ug_2 = UserGroup.objects.create(
            name="metropolis", title="Metropolis", type="district", collective_name=None
        )
        ug_3 = UserGroup.objects.create(name="human", title="Human", type="species", collective_name=None)

        url = reverse("user_groups")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 3)
        self.assertEqual(data_out[0]["name"], "gotham")
        self.assertEqual(data_out[0]["title"], "Gotham")
        self.assertEqual(data_out[0]["type"], "district")
        self.assertEqual(data_out[1]["name"], "metropolis")
        self.assertEqual(data_out[1]["title"], "Metropolis")
        self.assertEqual(data_out[1]["type"], "district")
        self.assertEqual(data_out[2]["name"], "human")
        self.assertEqual(data_out[2]["title"], "Human")
        self.assertEqual(data_out[2]["type"], "species")

        url = reverse("user_groups_by_type", args=["district"])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "gotham")
        self.assertEqual(data_out[0]["title"], "Gotham")
        self.assertEqual(data_out[0]["type"], "district")
        self.assertEqual(data_out[1]["name"], "metropolis")
        self.assertEqual(data_out[1]["title"], "Metropolis")
        self.assertEqual(data_out[1]["type"], "district")

        url = reverse("user_groups_by_type", args=["species"])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 1)
        self.assertEqual(data_out[0]["name"], "human")
        self.assertEqual(data_out[0]["title"], "Human")
        self.assertEqual(data_out[0]["type"], "species")

    def test_get_empty_list_if_no_user_groups(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        collective = Collective.objects.create(name="jla", title="JLA", creator=user)
        url = reverse("collective_user_groups", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)
