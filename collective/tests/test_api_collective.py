import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective


class CollectiveDetailViewTests(AuthTestCase):
    def test_get_collective_detail(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA', creator=user)
        response = client.get('/api/collective/jla/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], 'jla')
        self.assertEqual(data_out['title'], 'JLA')
        self.assertEqual(data_out['description'], None)
        self.assertEqual(data_out['creator'], user.username)

    def test_no_such_collective(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/collective/null/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_collective_info(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA', creator=user)
        data_in = {
            'name': 'section8',
            'title': 'Section 8',
            'description': 'Replaces old JLA'
        }
        response = client.put('/api/collective/jla/', data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['name'], 'section8')
        self.assertEqual(data_out['title'], 'Section 8')
        self.assertEqual(data_out['description'], 'Replaces old JLA')

    def test_create_collective(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(Collective.objects.count(), 0)
        data_in = {
            'name': 'jla',
            'title': 'JLA',
            'description': 'Justice League of America'
        }
        response = client.post('/api/collective/jla/', data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collective.objects.count(), 1)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, data_in['name'])
        self.assertEqual(collective.creator, user)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], data_in['name'])
        self.assertEqual(data_out['title'], data_in['title'])
        self.assertEqual(data_out['description'], data_in['description'])
        self.assertEqual(data_out['creator'], user.username)

    def test_create_collective_already_exists(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA')
        self.assertEqual(Collective.objects.count(), 1)
        data_in = {
            'name': 'jla',
            'title': 'JLA',
            'description': 'Justice League of America'
        }
        response = client.post('/api/collective/jla/', data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Collective.objects.count(), 1)

    def test_delete_collective(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(Collective.objects.count(), 1)
        response = client.delete('/api/collective/jla/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collective.objects.count(), 0)

    def test_delete_collective_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        creator = User.objects.create(username='batman', password='ImBatman')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA', creator=creator)
        self.assertEqual(Collective.objects.count(), 1)
        response = client.delete('/api/collective/jla/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collective.objects.count(), 1)
