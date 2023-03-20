import json
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import UserGroup


class GlobalSettingsViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse("settings"), "/api/settings/")

    def test_get_global_settings(self):
        client = APIClient()
        response = client.get(reverse("settings"))
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out["title"], "Atange")
        self.assertEqual(data_out["one_collective"], False)
        self.assertEqual(data_out["users_can_create_collectives"], False)
        self.assertEqual(data_out["require_names"], False)
