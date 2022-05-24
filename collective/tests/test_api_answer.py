import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem, Answer


class AnswerDetailViewTests(AuthTestCase):
    def test_reverse(self):
        self.assertEqual(reverse('answer', args=['jla', 'q1', 'superman']),
                         '/api/collective/jla/question/q1/answer/superman/')

    def test_get_answer_detail(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=user, vote=1, comment='Naturally')
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_out = json.loads(response.content.decode())
        # self.assertEqual(data_out['question'], 'q1')
        # self.assertEqual(data_out['user'], user.username)
        self.assertEqual(data_out['vote'], 1)
        self.assertEqual(data_out['comment'], 'Naturally')

    def test_no_such_answer(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=user)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1', creator=user)
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_answer(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=user, vote=1, comment='Naturally')
        self.assertEqual(Answer.objects.count(), 1)
        data_in = {
            'vote': -1,
            'comment': 'Actually maybe not'
        }
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.put(url, data_in)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.vote, -1)
        self.assertEqual(answer.comment, 'Actually maybe not')
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_out['vote'], -1)
        self.assertEqual(data_out['comment'], 'Actually maybe not')

    def test_update_answer_by_someone_else(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=creator, vote=1, comment='Naturally')
        self.assertEqual(Answer.objects.count(), 1)
        data_in = {
            'vote': -1,
            'comment': 'Actually maybe not'
        }
        url = reverse('answer', args=[collective.name, question.name, creator.username])
        response = client.put(url, data_in)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.vote, 1)
        self.assertEqual(answer.comment, 'Naturally')
        data_out = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data_out['detail'], 'Can edit only own answers')

    def test_create_answer(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        self.assertEqual(Answer.objects.count(), 0)
        data_in = {
            'vote': 1,
            'comment': 'Of course'
        }
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.user, user)
        self.assertEqual(answer.vote, data_in['vote'])
        self.assertEqual(answer.comment, data_in['comment'])
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['vote'], data_in['vote'])
        self.assertEqual(data_out['comment'], data_in['comment'])

    def test_create_answer_when_not_logged_in(self):
        client = APIClient()
        user = self.create_user()
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        self.assertEqual(Answer.objects.count(), 0)
        url = reverse('answer', args=[collective.name, question.name, user.username])
        data_in = {
            'vote': 1,
            'comment': 'Of course'
        }
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Answer.objects.count(), 0)
        data_out = json.loads(response.content.decode())
        self.assertEqual(data_out['detail'], 'Need to be logged in')

    def test_create_answer_already_exists(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=user, vote=1, comment='Of course')
        self.assertEqual(Answer.objects.count(), 1)
        data_in = {
            'vote': -1,
            'comment': 'Actually maybe not'
        }
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.post(url, data_in)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Answer.objects.count(), 1)
        answer = Answer.objects.first()
        self.assertEqual(answer.vote, 1)
        self.assertEqual(answer.comment, 'Of course')

    def test_delete_answer(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        creator = User.objects.create(username='batman', password='ImBatman')
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=user, vote=1, comment='Of course')
        self.assertEqual(Answer.objects.count(), 1)
        url = reverse('answer', args=[collective.name, question.name, user.username])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)

    def test_delete_answer_by_someone_else(self):
        client = APIClient()
        user = self.create_user()
        token = self.login(user)
        creator = User.objects.create(username='batman', password='ImBatman')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        collective = Collective.objects.create(name='jla', title='JLA', creator=creator)
        question = QuestionnaireItem.objects.create(collective=collective, name='q1', title='Question 1',
                                                    creator=creator)
        Answer.objects.create(question=question, user=creator, vote=1, comment='Of course')
        self.assertEqual(Answer.objects.count(), 1)
        url = reverse('answer', args=[collective.name, question.name, creator.username])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Answer.objects.count(), 1)
