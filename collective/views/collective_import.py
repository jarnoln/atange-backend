import json
import logging

from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.edit import FormView

from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from collective.models import Collective, QuestionnaireItem, Answer, Statistics


class UploadCollectiveForm(forms.Form):
    json_file = forms.FileField(label="Select Collective JSON file to upload")


def create_user(username):
    user = User.objects.create_user(username=username)
    return user


def parse_imported_data(data):
    creator_name = data['creator']
    logger = logging.getLogger(__name__)
    try:
        creator = User.objects.get(username=creator_name)
    except User.DoesNotExist:
        logger.warning('User {} does not exist'.format(creator_name))
        creator = create_user(creator_name)

    if Collective.objects.filter(name=data['name']).count() > 0:
        logger.warning('Collective with name {} already exists. Aborting import.'.format(data['name']))
        return None

    collective = Collective.objects.create(
        name=data['name'],
        title=data['title'],
        description=data['description'],
        is_visible=data['is_visible'],
        creator=creator
    )

    for question in data['questions']:
        try:
            question_creator = User.objects.get(username=question['creator'])
        except User.DoesNotExist:
            logger.warning('Question creator {} does not exist. Creating.'.format(creator_name))
            question_creator = create_user(creator_name)

        questionnaire_item = QuestionnaireItem.objects.create(
            collective=collective,
            name=question['name'],
            title=question['title'],
            description=question['description'],
            item_type=question['item_type'],
            order=question['order'],
            creator=question_creator
        )

        for answer in question['answers']:
            try:
                answer_user = User.objects.get(username=answer['user'])
            except User.DoesNotExist:
                logger.warning('Answer user {} does not exist. Creating.'.format(answer['user']))
                answer_user = create_user(answer['user'])

            answer_object = Answer.objects.create(
                question=questionnaire_item,
                user=answer_user,
                vote=answer['vote'],
                comment=answer['comment']
            )
    return collective


class CollectiveImportFormView(FormView):
    """Endpoint for importing new collective from uploaded JSON file"""
    "Using basic Django views"
    form_class = UploadCollectiveForm
    template_name = 'collective/upload.html'

    def form_valid(self, form):
        json_file = self.request.FILES['json_file']
        file_content = json_file.read()
        data = json.loads(file_content.decode('utf-8'))
        # logger = logging.getLogger(__name__)
        # logger.debug('Imported data: {}'.format(data))
        parse_imported_data(data)
        statistics = Statistics.objects.create()
        statistics.update()
        return super(CollectiveImportFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')


class CollectiveImport(APIView):
    """Endpoint for importing new collective from uploaded JSON file"""
    "Using Django REST API views"
    "Not yet used"
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveImport:post")
        logger.debug("  received_data: {}".format(request.data))
        response = Response()
        return response
