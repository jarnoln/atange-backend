import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class CollectiveAdminTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.creator = self.create_user()
        admin_group = UserGroup.objects.create(
            name="jla_admins", title="JLA administrators"
        )
        admin_group.add_member(self.creator)
        self.collective = Collective.objects.create(
            name="jla",
            title="JLA",
            description="",
            creator=self.creator,
            admin_group=admin_group,
        )
        self.url = reverse("collective_admins", args=[self.collective.name])

    def test_reverse(self):
        self.assertEqual(
            reverse("collective_admins", args=["jla"]),
            "/api/collective/jla/admins/",
        )

    def test_view_admins(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.collective.admin_group.members.count(), 1)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 1)
        self.assertEqual(data_out[0], "superman")
