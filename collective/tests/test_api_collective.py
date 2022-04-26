import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from .test_api_auth import AuthTestCase
from collective.models import Collective


class CollectiveDetailViewTests(AuthTestCase):
    def test_get_collective_detail(self):
        client = APIClient()
        token = self.login()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.get(username='superman')
        Collective.objects.create(name='jla', title='JLA', creator=creator)
        response = client.get('/api/collective/jla/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], 'jla')
        self.assertEqual(data_out['title'], 'JLA')
        self.assertEqual(data_out['description'], None)

    def test_no_such_collective(self):
        client = APIClient()
        token = self.login()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/collective/null/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
