import json
import logging

from django.shortcuts import get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView

from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


from collective.serializers import CollectiveExportSerializer
from collective.models import UserGroup, Collective, Statistics


class UploadCollectiveForm(forms.Form):
    json_file = forms.FileField(label="Select Collective JSON file to upload")


def create_user(username):
    user = User.objects.create_user(username=username)
    return user

def parse_imported_data(collective):
    creator_name = collective['creator']
    logger = logging.getLogger(__name__)
    try:
        creator = User.objects.get(username=creator_name)
    except User.DoesNotExist:
        logger.warning('User {} does not exist'.format(creator_name))
        creator = create_user(creator_name)

    if Collective.objects.filter(name=collective['name']).count() > 0:
        logger.warning('Collective with name {} already exists. Aborting import.'.format(collective['name']))
        return None

    collective = Collective.objects.create(
        name=collective['name'],
        title=collective['title'],
        description=collective['description'],
        is_visible=collective['is_visible'],
        creator=creator
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
        logger = logging.getLogger(__name__)
        logger.debug('Imported data: {}'.format(data))
        parse_imported_data(data)
        return super(CollectiveImportFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')


class CollectiveImport(APIView):
    """Endpoint for importing new collective from uploaded JSON file"""
    "Using Django REST API views"

    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveImport:post")
        logger.debug("  received_data: {}".format(request.data))
        response = Response()
        return response
