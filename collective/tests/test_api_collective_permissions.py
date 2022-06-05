import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective


class CollectivePermissionsTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("collective_permissions", args=["jla"]), "/api/collective/jla/permissions/")

    def test_get_collective_permissions_when_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        collective = Collective.objects.create(name="jla", title="JLA", description="", creator=user)
        response = client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], True)
        self.assertEqual(data_out["can_join"], False)

    def test_get_collective_permissions_when_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(name="jla", title="JLA", description="", creator=creator)
        response = client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], False)
        self.assertEqual(data_out["can_join"], False)

    def test_get_collective_permissions_when_not_logged_in(self):
        client = APIClient()
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(name="jla", title="JLA", description="", creator=creator)
        response = client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], False)
        self.assertEqual(data_out["can_join"], False)
