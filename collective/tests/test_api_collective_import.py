import json
from io import StringIO

from django.core.files.base import File
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .auth_test_case import AuthTestCase
from collective.models import Collective, QuestionnaireItem, Answer


class CollectiveImportFormViewTests(AuthTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.token = self.login(self.user)

    def test_reverse(self):
        self.assertEqual(reverse("collective_import_form"), "/upload/")

    def test_uses_correct_template(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(reverse("collective_import_form"))
        self.assertTemplateUsed(response, "collective/upload.html")

    def test_get_collective_import(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        url = reverse("collective_import_form")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_simple_collective(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        example_file = StringIO()
        collective = {
            'name': 'jsa',
            'title': 'JSA'
        }
        example_file.write(json.dumps(collective))
        file_object = File(example_file, name='collective.json')
        data = {'json_file': file_object}
        url = reverse("collective_import_form")
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
