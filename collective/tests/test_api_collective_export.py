import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class CollectiveExportViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.token = self.login(self.user)

    def test_reverse(self):
        self.assertEqual(reverse("collective_export", args=["jla"]), "/api/collective/jla/export/")

    def test_get_collective_export(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        collective = Collective.objects.create(
            name="jla", title="JLA", creator=self.user
        )
        url = reverse("collective_export", args=[collective.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["name"], "jla")
        self.assertEqual(data_out["title"], "JLA")
        self.assertEqual(data_out["description"], None)
        self.assertEqual(data_out["creator"], self.user.username)

    def test_no_such_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        url = reverse("collective_export", args=["unknown"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
