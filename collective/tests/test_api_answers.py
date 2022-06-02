import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem, Answer


class AnswerListViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(
            reverse("answers", args=["jla"]), "/api/collective/jla/answers/"
        )

    def test_get_answer_list(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        creator = User.objects.create(username="batman", password="ImBatman")
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
        Answer.objects.create(
            question=q_1, user=user, vote=1, comment="Of course"
        )
        Answer.objects.create(
            question=q_2, user=user, vote=-1, comment="Definitely not"
        )
        url = reverse("answers", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["question"], "q1")
        self.assertEqual(data_out[0]["user"], user.username)
        self.assertEqual(data_out[0]["vote"], 1)
        self.assertEqual(data_out[0]["comment"], "Of course")
        self.assertEqual(data_out[1]["question"], "q2")
        self.assertEqual(data_out[1]["user"], user.username)
        self.assertEqual(data_out[1]["vote"], -1)
        self.assertEqual(data_out[1]["comment"], "Definitely not")

    def test_get_empty_list_if_no_answers(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        creator = User.objects.create(username="batman", password="ImBatman")
        collective = Collective.objects.create(name="jla", title="JLA", creator=creator)
        QuestionnaireItem.objects.create(
            collective=collective,
            name="q1",
            title="Question 1",
            order=1,
            creator=creator,
        )
        QuestionnaireItem.objects.create(
            collective=collective,
            name="q2",
            title="Question 2",
            order=2,
            creator=creator,
        )
        url = reverse("answers", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)
