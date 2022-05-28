import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective


class CollectiveDetailViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('collective', args=['jla']), '/api/collective/jla/')

    def test_get_collective_detail(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        url = reverse('collective', args=[collective.name])
        response = client.get(url)
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
        url = reverse('collective', args=['unknown'])
        response = client.get(url)
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
        url = reverse('collective', args=['jla'])
        response = client.put(url, data_in)
        self.assertEqual(Collective.objects.count(), 1)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, data_in['name'])
        self.assertEqual(collective.title, data_in['title'])
        self.assertEqual(collective.description, data_in['description'])
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['name'], data_in['name'])
        self.assertEqual(data_out['title'], data_in['title'])
        self.assertEqual(data_out['description'], data_in['description'])

    def test_update_collective_when_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        data_in = {
            'name': 'section8',
            'title': 'Section 8',
            'description': 'Replaces old JLA'
        }
        url = reverse('collective', args=[collective.name])
        response = client.put(url, data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data_out['detail'], 'Only creator can edit')

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
        url = reverse('collective', args=['jla'])
        response = client.post(url, data_in)
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

    def test_create_when_not_logged_in(self):
        client = APIClient()
        self.assertEqual(Collective.objects.count(), 0)
        data_in = {
            'name': 'jla',
            'title': 'JLA',
            'description': 'Justice League of America'
        }
        url = reverse('collective', args=['jla'])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collective.objects.count(), 0)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['detail'], 'Need to be logged in')

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
        url = reverse('collective', args=['jla'])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Collective.objects.count(), 1)

    def test_delete_collective(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(Collective.objects.count(), 1)
        url = reverse('collective', args=[collective.name])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collective.objects.count(), 0)

    def test_delete_collective_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        creator = User.objects.create(username='batman', password='ImBatman')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        url = reverse('collective', args=[collective.name])
        self.assertEqual(Collective.objects.count(), 1)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Collective.objects.count(), 1)
