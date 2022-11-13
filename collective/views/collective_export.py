import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from collective.serializers import CollectiveSerializer, CollectiveExportSerializer
from collective.models import UserGroup, Collective, Statistics


class CollectiveExport(APIView):
    """Endpoint for collective operations"""

    def get(self, request, collective_name, format=None):
        logger = logging.getLogger(__name__)
        logger.debug("CollectiveExport:get collective_name:{}".format(collective_name))
        logger.debug(" request.user:{}".format(request.user))
        logger.debug(" format:{}".format(format))

        collective = get_object_or_404(Collective, name=collective_name)
        serializer = CollectiveSerializer(collective)
        return Response(serializer.data)
