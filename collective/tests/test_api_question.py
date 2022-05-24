import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem


class QuestionDetailViewTests(AuthTestCase):
    def test_get_question_detail(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        response = client.get('/api/collective/jla/question/q1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['name'], 'q1')
        self.assertEqual(data_out['title'], 'Question 1')
        self.assertEqual(data_out['description'], '')
        self.assertEqual(data_out['creator'], user.username)

    def test_no_such_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        Collective.objects.create(name='jla', title='JLA', creator=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get('/api/collective/jla/question/unknown/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        data_in = {
            'name': 'q2',
            'title': 'Question 2',
            'description': 'A simple question'
        }
        response = client.put('/api/collective/jla/question/q1/', data_in)
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
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=creator)
        data_in = {
            'name': 'q2',
            'title': 'Question 2',
            'description': 'A simple question'
        }
        response = client.put('/api/collective/jla/question/q1/', data_in)
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data_out['detail'], 'Only creator can edit')

    def test_create_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        data_in = {
            'name': 'q1',
            'title': 'Question 1',
            'description': 'Hard question'
        }
        response = client.post('/api/collective/jla/question/q1/', data_in)
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
        Collective.objects.create(name='jla', title='JLA', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        data_in = {
            'name': 'q1',
            'title': 'Question 1',
            'description': 'Hard question'
        }
        response = client.post('/api/collective/jla/question/q1/', data_in)
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
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        data_in = {
            'name': 'q1',
            'title': 'Question 2',
            'description': 'Very hard question'
        }
        response = client.post('/api/collective/jla/question/q1/', data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)

    def test_delete_question(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA')
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        response = client.delete('/api/collective/jla/question/q1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)

    def test_delete_collective_not_creator(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        creator = User.objects.create(username='batman', password='ImBatman')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=creator)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
        response = client.delete('/api/collective/jla/question/q1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(QuestionnaireItem.objects.count(), 1)
