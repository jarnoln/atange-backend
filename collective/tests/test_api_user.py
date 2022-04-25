import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .test_api_auth import AuthTestCase


class UserInfoViewTests(AuthTestCase):
    def test_get_user_info(self):
        client = APIClient()
        token = self.login()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/user/superman/')
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['email'], 'clark@dailyplanet.com')
        self.assertEqual(data_out['first_name'], 'Clark')
        self.assertEqual(data_out['last_name'], 'Kent')

    def test_no_such_user(self):
        client = APIClient()
        token = self.login()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/user/nobody/')
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_info(self):
        client = APIClient()
        token = self.login()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data_in = {
            'email': 'kalel@krypton.planet',
            'first_name': 'Kal',
            'last_name': 'El'
        }
        response = client.put('/api/user/superman/', data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['email'], 'kalel@krypton.planet')
        self.assertEqual(data_out['first_name'], 'Kal')
        self.assertEqual(data_out['last_name'], 'El')
