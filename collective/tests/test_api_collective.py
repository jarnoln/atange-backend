import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class CollectiveDetailViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.token = self.login(self.user)

    def test_reverse(self):
        self.assertEqual(reverse("collective", args=["jla"]), "/api/collective/jla/")

    def test_get_collective_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        collective = Collective.objects.create(
            name="jla", title="JLA", creator=self.user, is_visible=True
        )
        url = reverse("collective", args=[collective.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["name"], "jla")
        self.assertEqual(data_out["title"], "JLA")
        self.assertEqual(data_out["description"], None)
        self.assertEqual(data_out["creator"], self.user.username)
        self.assertEqual(data_out["is_visible"], True)

    def test_no_such_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        url = reverse("collective", args=["unknown"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_collective_info(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        Collective.objects.create(
            name="jla", title="JLA", creator=self.user, is_visible=True
        )
        data_in = {
            "name": "section8",
            "title": "Section 8",
            "description": "Replaces old JLA",
            "is_visible": False,
        }
        url = reverse("collective", args=["jla"])
        response = self.client.put(url, data_in)
        self.assertEqual(Collective.objects.count(), 1)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, data_in["name"])
        self.assertEqual(collective.title, data_in["title"])
        self.assertEqual(collective.description, data_in["description"])
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out["name"], data_in["name"])
        self.assertEqual(data_out["title"], data_in["title"])
        self.assertEqual(data_out["description"], data_in["description"])
        self.assertEqual(data_out["is_visible"], data_in["is_visible"])

    def test_update_collective_when_not_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(
            name="jla", title="JLA", creator=creator, is_visible=True
        )
        data_in = {
            "name": "section8",
            "title": "Section 8",
            "description": "Replaces old JLA",
            "is_visible": "false",
        }
        url = reverse("collective", args=[collective.name])
        response = self.client.put(url, data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data_out["detail"], "No permission to edit")

    def test_create_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(Collective.objects.count(), 0)
        data_in = {
            "name": "jla",
            "title": "JLA",
            "description": "Justice League of America",
        }
        url = reverse("collective", args=["jla"])
        response = self.client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collective.objects.count(), 1)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, data_in["name"])
        self.assertEqual(collective.creator, self.user)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["name"], data_in["name"])
        self.assertEqual(data_out["title"], data_in["title"])
        self.assertEqual(data_out["description"], data_in["description"])
        self.assertEqual(data_out["creator"], self.user.username)

    def test_create_collective_creates_also_member_and_admin_groups(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(Collective.objects.count(), 0)
        data_in = {"name": "jla", "title": "JLA", "description": ""}
        url = reverse("collective", args=["jla"])
        self.assertEqual(UserGroup.objects.count(), 0)
        response = self.client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collective.objects.count(), 1)
        self.assertEqual(UserGroup.objects.count(), 2)
        collective = Collective.objects.first()
        # Creator is automatically member of admin group but not member group
        self.assertFalse(collective.member_group.is_member(self.user))
        self.assertTrue(collective.admin_group.is_member(self.user))

    def test_create_when_not_logged_in(self):
        self.assertEqual(Collective.objects.count(), 0)
        data_in = {
            "name": "jla",
            "title": "JLA",
            "description": "Justice League of America",
        }
        url = reverse("collective", args=["jla"])
        response = self.client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collective.objects.count(), 0)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["detail"], "Need to be logged in")

    def test_create_collective_already_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        Collective.objects.create(name="jla", title="JLA")
        self.assertEqual(Collective.objects.count(), 1)
        data_in = {
            "name": "jla",
            "title": "JLA",
            "description": "Justice League of America",
        }
        url = reverse("collective", args=["jla"])
        response = self.client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Collective.objects.count(), 1)

    def test_delete_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        collective = Collective.objects.create(
            name="jla", title="JLA", creator=self.user
        )
        self.assertEqual(Collective.objects.count(), 1)
        url = reverse("collective", args=[collective.name])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collective.objects.count(), 0)

    def test_delete_collective_not_creator(self):
        creator = User.objects.create(username="batman", password="ImBatman")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        url = reverse("collective", args=[collective.name])
        self.assertEqual(Collective.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collective.objects.count(), 1)
