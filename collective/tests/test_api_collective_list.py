import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective


class CollectiveListViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("collectives"), "/api/collectives/")

    def test_get_collective_list(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        Collective.objects.create(name="jla", title="JLA", description="", creator=user)
        Collective.objects.create(name="jsa", title="JSA", description="", creator=user)
        response = client.get(reverse("collectives"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "jla")
        self.assertEqual(data_out[0]["title"], "JLA")
        self.assertEqual(data_out[0]["description"], "")
        self.assertTrue("is_visible" not in data_out[0])
        self.assertTrue("edited" not in data_out[0])
        self.assertEqual(data_out[0]["creator"], user.username)
        self.assertEqual(data_out[1]["name"], "jsa")
        self.assertEqual(data_out[1]["title"], "JSA")
        self.assertEqual(data_out[1]["creator"], user.username)
        self.assertEqual(data_out[1]["description"], "")

    def test_get_empty_list_if_no_collectives(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = client.get(reverse("collectives"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)

    def test_list_only_visible_collectives(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        Collective.objects.create(
            name="tfx", title="Tass Force X", creator=user, is_visible=False
        )
        response = client.get(reverse("collectives"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)
        Collective.objects.create(name="jla", title="JLA", creator=user)
        Collective.objects.create(name="jsa", title="JSA", creator=user)
        self.assertEqual(Collective.objects.count(), 3)
        response = client.get(reverse("collectives"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "jla")
        self.assertEqual(data_out[1]["name"], "jsa")
