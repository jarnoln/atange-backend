import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status


class RegisterViewTests(TestCase):
    def test_register_new_user(self):
        self.assertEqual(User.objects.count(), 0)
        data_in = {'username': 'superman', 'password': 'Man_of_Steel'}
        response = self.client.post('/auth/users/', data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['username'], 'superman')
        self.assertEqual(data_out['email'], '')


class LoginViewTests(TestCase):
    def test_login(self):
        user = User.objects.create_user(username='superman', password='Man_of_Steel')
        login_data = {'username': user.username, 'password': 'Man_of_Steel'}
        response = self.client.post('/auth/token/login/', login_data)
        self.assertEqual(response.status_code, 200)
        data_out = json.loads(response.content.decode())
        self.assertTrue('auth_token' in data_out)
