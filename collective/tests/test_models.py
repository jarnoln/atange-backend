from django.test import TestCase
from django.contrib.auth.models import User

from collective.models import Collective


class CollectiveModelTests(TestCase):
    def test_can_save_and_load(self):
        creator = User.objects.create_user(username='superman', password='Man_of_Steel')
        collective = Collective(name='jla', title="JLA", creator=creator)
        collective.save()
        self.assertEqual(Collective.objects.count(), 1)
        self.assertEqual(Collective.objects.first(), collective)

    def test_string(self):
        collective = Collective.objects.create(name='jla', title="JLA")
        self.assertEqual(str(collective), 'jla:JLA')
