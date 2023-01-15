import json
from io import StringIO

from django.contrib.auth.models import User
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
        collective = {"name": "jsa", "title": "JSA"}
        example_file.write(json.dumps(collective))
        file_object = File(example_file, name="collective.json")
        data = {"json_file": file_object}
        url = reverse("collective_import_form")

        self.assertEqual(Collective.objects.count(), 0)
        response = self.client.post(url, data, follow=True)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Collective.objects.count(), 1)

    def test_import_simple_collective_file(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        example_file = open("examples/test-collective.json", "r")
        file_object = File(example_file, name="collective.json")
        data = {"json_file": file_object}
        url = reverse("collective_import_form")

        self.assertEqual(Collective.objects.count(), 0)
        self.assertEqual(QuestionnaireItem.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)

        response = self.client.post(url, data, follow=True)
        example_file.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collective.objects.count(), 1)

        imported_file = open("examples/test-collective.json", "r")
        imported_data = json.load(imported_file)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, imported_data["name"])
        self.assertEqual(collective.title, imported_data["title"])
        self.assertEqual(collective.description, imported_data["description"])
        self.assertEqual(collective.is_visible, True)
        self.assertEqual(collective.creator.username, imported_data["creator"])

        self.assertEqual(QuestionnaireItem.objects.count(), 3)
        questionnaire_items = QuestionnaireItem.objects.all()
        h1 = questionnaire_items[0]
        q1 = questionnaire_items[1]
        q2 = questionnaire_items[2]
        self.assertEqual(h1.order, 0)
        self.assertEqual(h1.item_type, "H")
        self.assertEqual(h1.name, imported_data["questions"][0]["name"])
        self.assertEqual(h1.title, imported_data["questions"][0]["title"])
        self.assertEqual(h1.description, imported_data["questions"][0]["description"])
        self.assertEqual(h1.creator.username, imported_data["questions"][0]["creator"])
        self.assertEqual(q1.order, 1)
        self.assertEqual(q1.item_type, "Q")
        self.assertEqual(q2.order, 2)
        self.assertEqual(q2.item_type, "Q")

        self.assertEqual(Answer.objects.count(), 2)
        a1 = Answer.objects.get(question=q1)
        self.assertEqual(a1.user.username, "superman")
        self.assertEqual(a1.vote, -1)
        self.assertEqual(a1.comment, "")
        a2 = Answer.objects.get(question=q2)
        self.assertEqual(a2.user.username, "superman")
        self.assertEqual(a2.vote, 0)
        self.assertEqual(a2.comment, "")

    def test_import_collective_already_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        example_file = open("examples/test-collective.json", "r")
        file_object = File(example_file, name="collective.json")
        data = {"json_file": file_object}
        url = reverse("collective_import_form")
        Collective.objects.create(
            name="test-collective", title="Old test collective", creator=self.user
        )
        self.assertEqual(Collective.objects.count(), 1)
        response = self.client.post(url, data, follow=True)
        example_file.close()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collective.objects.count(), 1)

        imported_file = open("examples/test-collective.json", "r")
        imported_data = json.load(imported_file)
        collective = Collective.objects.first()
        self.assertEqual(collective.name, imported_data["name"])
        self.assertEqual(collective.title, "Old test collective")
