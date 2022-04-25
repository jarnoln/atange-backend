from django.test import TestCase
from django.urls import reverse

from collective.models import Collective


class IndexViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Index page')

    def test_shows_collectives(self):
        collective_1 = Collective.objects.create(name='jla', title='JLA')
        collective_2 = Collective.objects.create(name='jsa', title='JSA')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collective_1.name)
        self.assertContains(response, collective_2.name)


class CollectiveViewTests(TestCase):
    def test_collective_view(self):
        collective = Collective.objects.create(name='jla', title='JLA')
        response = self.client.get('/collective/jla/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'jla')