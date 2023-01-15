import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem, Answer


class CollectiveExportViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.token = self.login(self.user)

    def test_reverse(self):
        self.assertEqual(
            reverse("collective_export", args=["jla"]), "/api/collective/jla/export/"
        )

    def test_get_collective_export(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        creator = User.objects.create(username="batman", password="ImBatman")
        member = User.objects.create(username="aquaman", password="atlantis")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        q_1 = QuestionnaireItem.objects.create(
            collective=collective,
            name="q1",
            title="Question 1",
            order=1,
            creator=creator,
        )
        q_2 = QuestionnaireItem.objects.create(
            collective=collective,
            name="q2",
            title="Question 2",
            order=2,
            creator=creator,
        )
        Answer.objects.create(question=q_1, user=creator, vote=1, comment="Of course")
        Answer.objects.create(
            question=q_2, user=member, vote=-1, comment="Definitely not"
        )
        url = reverse("collective_export", args=[collective.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out["name"], "jla")
        self.assertEqual(data_out["title"], "JLA")
        self.assertEqual(data_out["description"], None)
        self.assertEqual(data_out["creator"], creator.username)
        questions = data_out["questions"]
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]["name"], "q1")
        self.assertEqual(len(questions[0]["answers"]), 1)
        self.assertEqual(questions[0]["answers"][0]["user"], "batman")
        self.assertEqual(questions[1]["name"], "q2")
        self.assertEqual(len(questions[1]["answers"]), 1)
        self.assertEqual(questions[1]["answers"][0]["user"], "aquaman")

    def test_no_such_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        url = reverse("collective_export", args=["unknown"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
