import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Answer, Collective, QuestionnaireItem


class QuestionListViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(
            reverse("questions", args=["jla"]), "/api/collective/jla/questions/"
        )

    def test_get_question_list(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        collective = Collective.objects.create(name="jla", title="JLA", creator=user)
        q_1 = QuestionnaireItem.objects.create(
            collective=collective, name="q1", title="Question 1", order=1, creator=user
        )
        q_2 = QuestionnaireItem.objects.create(
            collective=collective, name="q2", title="Question 2", order=2, creator=user
        )
        Answer.objects.create(question=q_1, user=user, vote=1, comment="Of course")
        Answer.objects.create(
            question=q_2, user=user, vote=-1, comment="Definitely not"
        )
        url = reverse("questions", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 2)
        self.assertEqual(data_out[0]["name"], "q1")
        self.assertEqual(data_out[0]["title"], "Question 1")
        self.assertEqual(data_out[0]["item_type"], "Q")
        self.assertEqual(data_out[0]["order"], 1)
        self.assertEqual(len(data_out[0]["answers"]), 1)
        self.assertEqual(data_out[1]["answers"][0]["user"], user.username)
        self.assertEqual(data_out[0]["answers"][0]["vote"], 1)
        self.assertEqual(data_out[0]["answers"][0]["comment"], "Of course")
        # self.assertEqual(data_out[0]['parent'], 'Question 1')
        self.assertEqual(data_out[0]["creator"], user.username)
        self.assertEqual(data_out[1]["name"], "q2")
        self.assertEqual(data_out[1]["title"], "Question 2")
        self.assertEqual(data_out[1]["item_type"], "Q")
        self.assertEqual(data_out[1]["order"], 2)
        self.assertEqual(data_out[1]["creator"], user.username)
        self.assertEqual(len(data_out[0]["answers"]), 1)
        self.assertEqual(data_out[1]["answers"][0]["user"], user.username)
        self.assertEqual(data_out[1]["answers"][0]["vote"], -1)
        self.assertEqual(data_out[1]["answers"][0]["comment"], "Definitely not")

    def test_get_empty_list_if_no_questions(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION="Token " + token)
        collective = Collective.objects.create(name="jla", title="JLA", creator=user)
        url = reverse("questions", args=[collective.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(len(data_out), 0)
