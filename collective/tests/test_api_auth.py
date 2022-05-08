import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase


class RegisterViewTests(TestCase):
    def test_register_new_user(self):
        client = APIClient()
        self.assertEqual(User.objects.count(), 0)
        data_in = {'username': 'superman', 'password': 'Man_of_Steel'}
        response = client.post('/auth/users/', data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['username'], 'superman')
        self.assertEqual(data_out['email'], '')


class DeleteUserViewTests(AuthTestCase):
    def delete_user(self):
        client = APIClient()
        user = self.create_user()
        self.login(user)
        self.assertEqual(User.objects.count(), 1)
        response = client.delete('/users/me/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class LoginViewTests(TestCase):
    def test_login(self):
        client = APIClient()
        user = User.objects.create_user(username='superman', password='Man_of_Steel')
        login_data = {'username': user.username, 'password': 'Man_of_Steel'}
        response = client.post('/auth/token/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertTrue('auth_token' in data_out)
        self.assertEqual(len(data_out['auth_token']), 40)


class UserDetailViewTests(AuthTestCase):
    def test_user_details(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['username'], user.username)
        self.assertEqual(data_out['email'], user.email)

    def test_user_details_no_auth(self):
        client = APIClient()
        response = client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTests(AuthTestCase):
    def test_logout(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post('/auth/token/logout/', {})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_no_auth(self):
        client = APIClient()
        response = client.post('/auth/token/logout/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
