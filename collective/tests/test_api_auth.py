import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/users/"
        self.data_in = {"username": "superman", "password": "Man_of_Steel"}

    def test_register_new_user(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(self.url, self.data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["username"], "superman")
        self.assertEqual(data_out["email"], "")

    def test_register_user_already_exists(self):
        User.objects.create(username="superman")
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(self.url, self.data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        data_out = json.loads(response.content.decode())
        self.assertEqual(
            data_out["username"], ["A user with that username already exists."]
        )


class DeleteUserViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/users/me/"
        self.data_in = {"current_password": "Man_of_Steel"}

    def test_delete_user(self):
        user = self.create_user()
        token = self.login(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.url, self.data_in)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_delete_user_not_logged_in(self):
        User.objects.create(username="superman")
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.url, self.data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_no_token(self):
        user = self.create_user()
        self.login(user)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.url, self.data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_no_password(self):
        user = self.create_user()
        token = self.login(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_wrong_password(self):
        user = self.create_user()
        token = self.login(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.url, {'current_password': 'wrong_password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/token/login/"
        self.login_data = {"username": "superman", "password": "Man_of_Steel"}

    def test_login(self):
        User.objects.create_user(username="superman", password="Man_of_Steel")
        response = self.client.post(self.url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertTrue("auth_token" in data_out)
        self.assertEqual(len(data_out["auth_token"]), 40)

    def test_login_no_such_user(self):
        response = self.client.post(self.url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_out = json.loads(response.content.decode())
        self.assertFalse("auth_token" in data_out)
        self.assertEqual(
            data_out["non_field_errors"],
            ["Unable to log in with provided credentials."],
        )

    def test_login_wrong_password(self):
        User.objects.create_user(username="superman", password="Man_of_Steel")
        login_data = {"username": "superman", "password": "Man_of_Iron"}
        response = self.client.post(self.url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_out = json.loads(response.content.decode())
        self.assertFalse("auth_token" in data_out)
        self.assertEqual(
            data_out["non_field_errors"],
            ["Unable to log in with provided credentials."],
        )


class UserDetailViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/users/me/"

    def test_user_details(self):
        user = self.create_user()
        token = self.login(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["username"], user.username)
        self.assertEqual(data_out["email"], user.email)

    def test_user_details_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/auth/token/logout/"

    def test_logout(self):
        user = self.create_user()
        token = self.login(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post("/auth/token/logout/", {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_no_auth(self):
        response = self.client.post("/auth/token/logout/", {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
