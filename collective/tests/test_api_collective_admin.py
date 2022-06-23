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
        token = self.login(self.creator)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
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
        self.user = User.objects.create(username="batman", password="ImBatman")
        self.url = reverse(
            "collective_admin", args=[self.collective.name, self.user.username]
        )

    def test_reverse(self):
        self.assertEqual(
            reverse("collective_admin", args=["jla", "batman"]),
            "/api/collective/jla/admin/batman/",
        )

    def test_add_user_to_admins(self):
        self.assertEqual(self.collective.admin_group.members.count(), 1)
        self.assertFalse(self.collective.admin_group.is_member(self.user))
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.collective.admin_group.members.count(), 2)
        self.assertTrue(self.collective.admin_group.is_member(self.user))

    def test_remove_user_from_admins(self):
        self.collective.admin_group.add_member(self.user)
        self.assertEqual(self.collective.admin_group.members.count(), 2)
        self.assertTrue(self.collective.admin_group.is_member(self.user))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.collective.admin_group.members.count(), 1)
        self.assertFalse(self.collective.admin_group.is_member(self.user))
