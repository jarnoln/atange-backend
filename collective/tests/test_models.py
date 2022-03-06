from django.test import TestCase
from collective.models import Collective


class CollectiveModelTests(TestCase):
    def test_can_save_and_load(self):
        collective = Collective(name='jla', title="JLA")
        collective.save()
        self.assertEqual(Collective.objects.count(), 1)
        self.assertEqual(Collective.objects.first(), collective)
