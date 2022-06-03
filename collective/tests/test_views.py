from django.test import TestCase
from django.urls import reverse

from collective.models import Statistics


class IndexViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atange backend")

    def test_shows_statistics(self):
        Statistics.objects.create()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statistics")
