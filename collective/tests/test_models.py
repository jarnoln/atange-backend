from django.test import TestCase
from django.contrib.auth.models import User

from collective.models import Collective, QuestionnaireItem


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


class QuestionnaireItemModelTests(TestCase):
    def test_can_save_and_load(self):
        creator = User.objects.create_user(username='superman', password='Man_of_Steel')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        item = QuestionnaireItem(collective=collective, name='Q1', title='Question 1')
        item.save()
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        self.assertEqual(QuestionnaireItem.objects.first(), item)

    def test_string(self):
        creator = User.objects.create_user(username='superman', password='Man_of_Steel')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        item = QuestionnaireItem.objects.create(collective=collective, name='Q1', title='Question 1')
        self.assertEqual(str(item), 'jla:Q:Q1:Question 1')

    def test_default_values(self):
        creator = User.objects.create_user(username='superman', password='Man_of_Steel')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        item = QuestionnaireItem.objects.create(collective=collective, name='Q1', title='Question 1')
        self.assertEqual(item.description, '')
        self.assertEqual(item.order, 0)
        self.assertEqual(item.creator, None)
        self.assertEqual(item.item_type, 'Q')
        self.assertEqual(item.parent, None)
