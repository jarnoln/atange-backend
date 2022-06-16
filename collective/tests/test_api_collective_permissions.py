import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class CollectivePermissionsTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.token = self.login(self.user)

    def test_reverse(self):
        self.assertEqual(
            reverse("collective_permissions", args=["jla"]),
            "/api/collective/jla/permissions/",
        )

    def test_get_collective_permissions_when_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        collective = Collective.objects.create(
            name="jla", title="JLA", description="", creator=self.user
        )
        response = self.client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], True)
        self.assertEqual(data_out["can_join"], False)

    def test_get_collective_permissions_when_not_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(
            name="jla", title="JLA", description="", creator=creator
        )
        response = self.client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], False)
        self.assertEqual(data_out["can_join"], False)

    def test_get_collective_permissions_when_not_creator_but_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(
            name="jla", title="JLA", description="", creator=creator
        )
        admin_group = UserGroup.objects.create(name='jla_admins', title='JLA administrators')
        admin_group.add_member(self.user)
        collective.admin_group = admin_group
        collective.save()
        response = self.client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], True)
        self.assertEqual(data_out["can_join"], False)

    def test_get_collective_permissions_when_not_logged_in(self):
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(
            name="jla", title="JLA", description="", creator=creator
        )
        response = self.client.get(reverse("collective_permissions", args=[collective.name]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["can_edit"], False)
        self.assertEqual(data_out["can_join"], False)
