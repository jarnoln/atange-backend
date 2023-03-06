import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, UserGroup


class UserGroupTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        token = self.login(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.collective = Collective.objects.create(
            name="jla", title="JLA", description="", creator=self.user
        )
        self.user_group = UserGroup.objects.create(
            name="gotham",
            title="Gotham",
            type="district",
            collective_name=self.collective.name,
        )

    def test_reverse(self):
        self.assertEqual(
            reverse("collective_user_group_members", args=["jla", "gotham"]),
            "/api/collective/jla/group/gotham/members/",
        )

        self.assertEqual(
            reverse("collective_user_group_join", args=["jla", "gotham"]),
            "/api/collective/jla/group/gotham/join/",
        )

        self.assertEqual(
            reverse("collective_user_group_leave", args=["jla", "gotham"]),
            "/api/collective/jla/group/gotham/leave/",
        )

    def test_list_group_members(self):
        url = reverse(
            "collective_user_group_members",
            args=[self.collective.name, self.user_group.name],
        )
        self.assertEqual(self.user_group.members.count(), 0)
        self.assertFalse(self.user_group.is_member(self.user))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)

        self.user_group.add_member(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 1)
        self.assertEqual(data_out[0], self.user.username)

    def test_join_group(self):
        url = reverse(
            "collective_user_group_join",
            args=[self.collective.name, self.user_group.name],
        )
        self.assertEqual(self.user_group.members.count(), 0)
        self.assertFalse(self.user_group.is_member(self.user))
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user_group.members.count(), 1)
        self.assertTrue(self.user_group.is_member(self.user))

    def test_leave_group(self):
        url = reverse(
            "collective_user_group_leave",
            args=[self.collective.name, self.user_group.name],
        )
        self.user_group.add_member(self.user)
        self.assertEqual(self.user_group.members.count(), 1)
        self.assertTrue(self.user_group.is_member(self.user))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user_group.members.count(), 0)
        self.assertFalse(self.user_group.is_member(self.user))
