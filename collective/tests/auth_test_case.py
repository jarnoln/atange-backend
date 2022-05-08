import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class AuthTestCase(TestCase):
    """ Base test class with some helper methods for authentication"""
    def create_user(self):
        user = User.objects.create_user(
            username='superman',
            password='Man_of_Steel',
            email='clark@dailyplanet.com',
            first_name='Clark',
            last_name='Kent'
        )
        return user

    def login(self, user):
        client = APIClient()
        login_data = {'username': user.username, 'password': 'Man_of_Steel'}
        response = client.post('/auth/token/login/', login_data)
        data_out = json.loads(response.content.decode())
        token = data_out['auth_token']
        return token
