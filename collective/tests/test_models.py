from django.test import TestCase
from django.contrib.auth.models import User

from collective.models import UserGroup, Membership, Collective, QuestionnaireItem, Answer, Statistics


class UserGroupModelTests(TestCase):
    def test_can_save_and_load(self):
        user_group = UserGroup(name="admins", title="Administrators")
        user_group.save()
        self.assertEqual(UserGroup.objects.count(), 1)
        self.assertEqual(UserGroup.objects.first(), user_group)

    def test_string(self):
        user_group = UserGroup.objects.create(name="admins", title="Admins")
        self.assertEqual(str(user_group), "admins:Admins")

    def test_adding_members(self):
        admins = UserGroup.objects.create(name="admins", title="Admins")
        self.assertEqual(admins.members.count(), 0)
        user_1 = User.objects.create_user(username="superman", password="Man_of_Steel")
        self.assertFalse(admins.is_member(user_1))
        admins.add_member(user_1)
        self.assertTrue(admins.is_member(user_1))
        self.assertEqual(admins.members.count(), 1)
        user_2 = User.objects.create_user(username="batman", password="ImBatman")
        self.assertFalse(admins.is_member(user_2))
        admins.add_member(user_2)
        self.assertTrue(admins.is_member(user_2))
        self.assertEqual(admins.members.count(), 2)

    def test_kicking_members(self):
        admins = UserGroup.objects.create(name="admins", title="Admins")
        user_1 = User.objects.create_user(username="superman", password="Man_of_Steel")
        user_2 = User.objects.create_user(username="batman", password="ImBatman")
        admins.add_member(user_1)
        admins.add_member(user_2)
        self.assertTrue(admins.is_member(user_1))
        self.assertTrue(admins.is_member(user_2))
        self.assertEqual(admins.members.count(), 2)
        admins.kick_member(user_1)
        self.assertEqual(admins.members.count(), 1)
        self.assertFalse(admins.is_member(user_1))
        self.assertTrue(admins.is_member(user_2))
        admins.kick_member(user_2)
        self.assertEqual(admins.members.count(), 0)
        self.assertFalse(admins.is_member(user_1))
        self.assertFalse(admins.is_member(user_2))


class MembershipModelTests(TestCase):
    def test_can_save_and_load(self):
        user = User.objects.create_user(username="superman", password="Man_of_Steel")
        user_group = UserGroup.objects.create(name="admins", title="Admins")
        membership = Membership(user=user, group=user_group)
        membership.save()
        self.assertEqual(Membership.objects.count(), 1)
        self.assertEqual(Membership.objects.first(), membership)

    def test_string(self):
        user = User.objects.create_user(username="superman", password="Man_of_Steel")
        user_group = UserGroup.objects.create(name="admins", title="Admins")
        membership = Membership.objects.create(user=user, group=user_group)
        self.assertEqual(str(membership), "superman:admins")


class CollectiveModelTests(TestCase):
    def test_can_save_and_load(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective(name="jla", title="JLA", creator=creator)
        collective.save()
        self.assertEqual(Collective.objects.count(), 1)
        self.assertEqual(Collective.objects.first(), collective)

    def test_string(self):
        collective = Collective.objects.create(name="jla", title="JLA")
        self.assertEqual(str(collective), "jla:JLA")


class QuestionnaireItemModelTests(TestCase):
    def test_can_save_and_load(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        item = QuestionnaireItem(collective=collective, name="Q1", title="Question 1")
        item.save()
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        self.assertEqual(QuestionnaireItem.objects.first(), item)

    def test_string(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        item = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        self.assertEqual(str(item), "jla:Q:Q1:Question 1")

    def test_default_values(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        item = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        self.assertEqual(item.description, "")
        self.assertEqual(item.order, 0)
        self.assertEqual(item.creator, None)
        self.assertEqual(item.item_type, "Q")
        self.assertEqual(item.parent, None)


class AnswerModelTests(TestCase):
    def test_can_save_and_load(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        question = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        answer = Answer(question=question, user=creator)
        answer.save()
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.first(), answer)

    def test_string(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        question = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        answer = Answer.objects.create(question=question, user=creator)
        self.assertEqual(str(answer), "jla:superman:Question 1:0")

    def test_default_values(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        question = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        answer = Answer.objects.create(question=question, user=creator)
        self.assertEqual(answer.comment, "")
        self.assertEqual(answer.vote, 0)


class StatisticsModelTests(TestCase):
    def test_can_save_and_load(self):
        statistics = Statistics()
        statistics.save()
        self.assertEqual(Statistics.objects.count(), 1)
        self.assertEqual(Statistics.objects.first(), statistics)

    def test_string(self):
        statistics = Statistics.objects.create()
        timestamp_string = str(statistics.created)
        self.assertEqual(str(statistics), "{}:0:0:0:0".format(timestamp_string))

    def test_default_values(self):
        creator = User.objects.create_user(username="superman", password="Man_of_Steel")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        question = QuestionnaireItem.objects.create(
            collective=collective, name="Q1", title="Question 1"
        )
        Answer.objects.create(question=question, user=creator)
        statistics = Statistics.objects.create()
        statistics.update()
        self.assertEqual(statistics.collectives, 1)
        self.assertEqual(statistics.questions, 1)
        self.assertEqual(statistics.answers, 1)
        self.assertEqual(statistics.users, 1)
