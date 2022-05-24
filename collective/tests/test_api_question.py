import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem, Answer


class QuestionDetailViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('question', args=['jla', 'q1']), '/api/collective/jla/question/q1/')

    def test_get_question_detail(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        answer = Answer.objects.create(question=question, user=user, vote=1, comment='Of course')
        url = reverse('question', args=[collective.name, question.name])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], 'q1')
        self.assertEqual(data_out['title'], 'Question 1')
        self.assertEqual(data_out['description'], '')
        self.assertEqual(data_out['creator'], user.username)
        self.assertEqual(len(data_out['answers']), 1)
        self.assertEqual(data_out['answers'][0]['vote'], answer.vote)
        self.assertEqual(data_out['answers'][0]['comment'], answer.comment)

    def test_no_such_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        url = reverse('question', args=[collective.name, 'unknown'])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        data_in = {
            'name': 'q2',
            'title': 'Question 2',
            'description': 'A simple question'
        }
        url = reverse('question', args=[collective.name, question.name])
        response = client.put(url, data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['name'], 'q2')
        self.assertEqual(data_out['title'], 'Question 2')
        self.assertEqual(data_out['description'], 'A simple question')

    def test_update_question_when_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        data_in = {
            'name': 'q2',
            'title': 'Question 2',
            'description': 'A simple question'
        }
        url = reverse('question', args=[collective.name, question.name])
        response = client.put(url, data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data_out['detail'], 'Only creator can edit')

    def test_create_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        data_in = {
            'name': 'q1',
            'title': 'Question 1',
            'description': 'Hard question'
        }
        url = reverse('question', args=[collective.name, 'q1'])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        question = QuestionnaireItem.objects.first()
        self.assertEqual(question.name, data_in['name'])
        self.assertEqual(question.creator, user)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], data_in['name'])
        self.assertEqual(data_out['title'], data_in['title'])
        self.assertEqual(data_out['description'], data_in['description'])
        self.assertEqual(data_out['creator'], user.username)

    def test_create_when_not_logged_in(self):
        client = APIClient()
        user = self.create_user()
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        data_in = {
            'name': 'q1',
            'title': 'Question 1',
            'description': 'Hard question'
        }
        url = reverse('question', args=[collective.name, 'q1'])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['detail'], 'Need to be logged in')

    def test_create_question_already_exists(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA')
        q_1 = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        data_in = {
            'name': 'q1',
            'title': 'Question 2',
            'description': 'Very hard question'
        }
        url = reverse('question', args=[collective.name, q_1.name])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)

    def test_delete_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA')
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        url = reverse('question', args=[collective.name, question.name])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)

    def test_delete_collective_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        creator = User.objects.create(username='batman', password='ImBatman')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        url = reverse('question', args=[collective.name, question.name])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
